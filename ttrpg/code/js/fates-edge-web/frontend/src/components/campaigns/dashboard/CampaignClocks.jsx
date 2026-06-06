// frontend/src/components/campaigns/dashboard/CampaignClocks.jsx (enhanced)
import React, { useState } from 'react';
import { useCampaignStore } from '../../../store/campaignStore';

const CampaignClocks = ({ timers, isGM }) => {
  const { updateCampaign, currentCampaign } = useCampaignStore();
  const [editingClock, setEditingClock] = useState(null);
  const [editForm, setEditForm] = useState({ name: '', segments: 8, progress: 0 });

  const handleTickClock = async (timerId) => {
    if (!isGM || !currentCampaign) return;
    
    try {
      const timer = timers.find(c => c.timerid === timerId);
      if (!timer) return;
      
      const newProgress = Math.min(timer.progress + 1, timer.segments);
      const updatedClocks = timers.map(c => 
        c.timerid === timerId ? { ...c, progress: newProgress } : c
      );
      
      await updateCampaign(currentCampaign.campaignid, { timers: updatedClocks });
    } catch (error) {
      console.error('Failed to tick timer:', error);
    }
  };

  const handleResetClock = async (timerId) => {
    if (!isGM || !currentCampaign) return;
    
    try {
      const updatedClocks = timers.map(c => 
        c.timerid === timerId ? { ...c, progress: 0 } : c
      );
      
      await updateCampaign(currentCampaign.campaignid, { timers: updatedClocks });
    } catch (error) {
      console.error('Failed to reset timer:', error);
    }
  };

  const handleEditClock = (timer) => {
    setEditingClock(timer.timerid);
    setEditForm({
      name: timer.name,
      segments: timer.segments,
      progress: timer.progress
    });
  };

  const handleSaveEdit = async () => {
    if (!isGM || !currentCampaign || !editingClock) return;
    
    try {
      const updatedClocks = timers.map(c => 
        c.timerid === editingClock ? { ...c, ...editForm } : c
      );
      
      await updateCampaign(currentCampaign.campaignid, { timers: updatedClocks });
      setEditingClock(null);
    } catch (error) {
      console.error('Failed to update timer:', error);
    }
  };

  const handleDeleteClock = async (timerId) => {
    if (!isGM || !currentCampaign) return;
    
    try {
      const updatedClocks = timers.filter(c => c.timerid !== timerId);
      await updateCampaign(currentCampaign.campaignid, { timers: updatedClocks });
    } catch (error) {
      console.error('Failed to delete timer:', error);
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
      
      const updatedClocks = [...timers, newClock];
      await updateCampaign(currentCampaign.campaignid, { timers: updatedClocks });
    } catch (error) {
      console.error('Failed to add timer:', error);
    }
  };

  const renderClock = (timer) => {
    if (editingClock === timer.timerid) {
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
          <h3 className="font-medium text-fate-accent">{timer.name}</h3>
          {isGM && (
            <div className="flex space-x-1">
              <button
                onClick={() => handleEditClock(timer)}
                className="text-xs bg-gray-700 hover:bg-gray-600 text-gray-300 px-2 py-1 rounded"
              >
                Edit
              </button>
              <button
                onClick={() => handleDeleteClock(timer.timerid)}
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
            <span>{timer.progress}/{timer.segments}</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-fate-accent h-2 rounded-full transition-all duration-300"
              style={{ width: `${(timer.progress / timer.segments) * 100}%` }}
            ></div>
          </div>
        </div>
        
        {isGM && (
          <div className="flex space-x-2">
            <button
              onClick={() => handleTickClock(timer.timerid)}
              disabled={timer.progress >= timer.segments}
              className="btn-primary text-sm px-3 py-1 disabled:opacity-50"
            >
              Tick
            </button>
            <button
              onClick={() => handleResetClock(timer.timerid)}
              disabled={timer.progress === 0}
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
      
      {timers && timers.length > 0 ? (
        <div className="space-y-4">
          {timers.map((timer) => (
            <div key={timer.timerid || `${timer.name}-${timer.segments}`}>
              {renderClock(timer)}
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-fate-dark rounded-lg p-6 text-center">
          <p className="text-gray-400 mb-3">No campaign timers yet</p>
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

