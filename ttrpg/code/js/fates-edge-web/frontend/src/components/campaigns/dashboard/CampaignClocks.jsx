// frontend/src/components/campaigns/dashboard/CampaignClocks.jsx (enhanced)
import React, { useState } from 'react';
import { useCampaignStore } from '../../../store/campaignStore';

const CampaignClocks = ({ clocks, isGM }) => {
  const { updateCampaign, currentCampaign } = useCampaignStore();
  const [editingClock, setEditingClock] = useState(null);
  const [editForm, setEditForm] = useState({ name: '', segments: 8, progress: 0 });

  const handleTickClock = async (clockId) => {
    if (!isGM || !currentCampaign) return;
    
    try {
      const clock = clocks.find(c => c.clockid === clockId);
      if (!clock) return;
      
      const newProgress = Math.min(clock.progress + 1, clock.segments);
      const updatedClocks = clocks.map(c => 
        c.clockid === clockId ? { ...c, progress: newProgress } : c
      );
      
      await updateCampaign(currentCampaign.campaignid, { clocks: updatedClocks });
    } catch (error) {
      console.error('Failed to tick clock:', error);
    }
  };

  const handleResetClock = async (clockId) => {
    if (!isGM || !currentCampaign) return;
    
    try {
      const updatedClocks = clocks.map(c => 
        c.clockid === clockId ? { ...c, progress: 0 } : c
      );
      
      await updateCampaign(currentCampaign.campaignid, { clocks: updatedClocks });
    } catch (error) {
      console.error('Failed to reset clock:', error);
    }
  };

  const handleEditClock = (clock) => {
    setEditingClock(clock.clockid);
    setEditForm({
      name: clock.name,
      segments: clock.segments,
      progress: clock.progress
    });
  };

  const handleSaveEdit = async () => {
    if (!isGM || !currentCampaign || !editingClock) return;
    
    try {
      const updatedClocks = clocks.map(c => 
        c.clockid === editingClock ? { ...c, ...editForm } : c
      );
      
      await updateCampaign(currentCampaign.campaignid, { clocks: updatedClocks });
      setEditingClock(null);
    } catch (error) {
      console.error('Failed to update clock:', error);
    }
  };

  const handleDeleteClock = async (clockId) => {
    if (!isGM || !currentCampaign) return;
    
    try {
      const updatedClocks = clocks.filter(c => c.clockid !== clockId);
      await updateCampaign(currentCampaign.campaignid, { clocks: updatedClocks });
    } catch (error) {
      console.error('Failed to delete clock:', error);
    }
  };

  const handleAddClock = async () => {
    if (!isGM || !currentCampaign) return;
    
    try {
      const newClock = {
        name: 'New Clock',
        segments: 8,
        progress: 0
      };
      
      const updatedClocks = [...clocks, newClock];
      await updateCampaign(currentCampaign.campaignid, { clocks: updatedClocks });
    } catch (error) {
      console.error('Failed to add clock:', error);
    }
  };

  const renderClock = (clock) => {
    if (editingClock === clock.clockid) {
      return (
        <div className="bg-fate-dark rounded-lg p-4">
          <input
            type="text"
            value={editForm.name}
            onChange={(e) => setEditForm({...editForm, name: e.target.value})}
            className="input-field w-full mb-2"
          />
          <div className="flex items-center space-x-2 mb-2">
            <label className="text-sm text-gray-300">Segments:</label>
            <select
              value={editForm.segments}
              onChange={(e) => setEditForm({...editForm, segments: parseInt(e.target.value)})}
              className="input-field"
            >
              {[4, 6, 8, 10, 12].map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
          <div className="flex items-center space-x-2 mb-3">
            <label className="text-sm text-gray-300">Progress:</label>
            <input
              type="number"
              min="0"
              max={editForm.segments}
              value={editForm.progress}
              onChange={(e) => setEditForm({...editForm, progress: parseInt(e.target.value) || 0})}
              className="input-field w-20"
            />
            <span className="text-sm text-gray-400">/ {editForm.segments}</span>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleSaveEdit}
              className="btn-primary text-sm px-3 py-1"
            >
              Save
            </button>
            <button
              onClick={() => setEditingClock(null)}
              className="btn-secondary text-sm px-3 py-1"
            >
              Cancel
            </button>
          </div>
        </div>
      );
    }

    return (
      <div className="bg-fate-dark rounded-lg p-4">
        <div className="flex justify-between items-start mb-3">
          <h3 className="font-medium text-fate-accent">{clock.name}</h3>
          {isGM && (
            <div className="flex space-x-1">
              <button
                onClick={() => handleEditClock(clock)}
                className="text-xs bg-gray-700 hover:bg-gray-600 text-gray-300 px-2 py-1 rounded"
              >
                Edit
              </button>
              <button
                onClick={() => handleDeleteClock(clock.clockid)}
                className="text-xs bg-red-900 hover:bg-red-800 text-red-200 px-2 py-1 rounded"
              >
                Delete
              </button>
            </div>
          )}
        </div>
        
        <div className="mb-3">
          <div className="flex justify-between text-sm text-gray-400 mb-1">
            <span>Progress</span>
            <span>{clock.progress}/{clock.segments}</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-fate-accent h-2 rounded-full transition-all duration-300"
              style={{ width: `${(clock.progress / clock.segments) * 100}%` }}
            ></div>
          </div>
        </div>
        
        {isGM && (
          <div className="flex space-x-2">
            <button
              onClick={() => handleTickClock(clock.clockid)}
              disabled={clock.progress >= clock.segments}
              className="btn-primary text-sm px-3 py-1 disabled:opacity-50"
            >
              Tick
            </button>
            <button
              onClick={() => handleResetClock(clock.clockid)}
              disabled={clock.progress === 0}
              className="btn-secondary text-sm px-3 py-1 disabled:opacity-50"
            >
              Reset
            </button>
          </div>
        )}
      </div>
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold text-fate-accent">Campaign Clocks</h3>
        {isGM && (
          <button
            onClick={handleAddClock}
            className="text-sm bg-fate-accent hover:bg-fate-primary text-fate-darker px-3 py-1 rounded-lg"
          >
            Add Clock
          </button>
        )}
      </div>
      
      {clocks && clocks.length > 0 ? (
        <div className="space-y-4">
          {clocks.map((clock) => (
            <div key={clock.clockid || `${clock.name}-${clock.segments}`}>
              {renderClock(clock)}
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-fate-dark rounded-lg p-6 text-center">
          <p className="text-gray-400 mb-3">No campaign clocks yet</p>
          {isGM && (
            <button
              onClick={handleAddClock}
              className="btn-primary"
            >
              Create Clock
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default CampaignClocks;

