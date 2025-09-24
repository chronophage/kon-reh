import React, { useState } from 'react';
import { useCharacterStore } from '../../../../store/characterStore';
import { PlusIcon, TrashIcon, PencilIcon } from '@heroicons/react/24/outline';

const FollowersTab = ({ character }) => {
  const { updateCharacter } = useCharacterStore();
  const [followers, setFollowers] = useState(character.followers || []);
  const [newFollower, setNewFollower] = useState({ name: '', cap: 1, condition: 'Maintained' });
  const [editingIndex, setEditingIndex] = useState(null);
  const [editFollower, setEditFollower] = useState({ name: '', cap: 1, condition: 'Maintained' });
  const [isSaving, setIsSaving] = useState(false);

  const conditions = ['Maintained', 'Neglected', 'Compromised'];

  const handleAddFollower = async () => {
    if (!newFollower.name.trim()) return;
    
    const updatedFollowers = [...followers, newFollower];
    setFollowers(updatedFollowers);
    setNewFollower({ name: '', cap: 1, condition: 'Maintained' });
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { followers: updatedFollowers });
    } catch (error) {
      console.error('Failed to add follower:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleEditFollower = (index) => {
    setEditingIndex(index);
    setEditFollower({ ...followers[index] });
  };

  const handleSaveEdit = async () => {
    if (!editFollower.name.trim()) return;
    
    const updatedFollowers = [...followers];
    updatedFollowers[editingIndex] = editFollower;
    setFollowers(updatedFollowers);
    setEditingIndex(null);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { followers: updatedFollowers });
    } catch (error) {
      console.error('Failed to update follower:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteFollower = async (index) => {
    const updatedFollowers = followers.filter((_, i) => i !== index);
    setFollowers(updatedFollowers);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { followers: updatedFollowers });
    } catch (error) {
      console.error('Failed to delete follower:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const getConditionColor = (condition) => {
    switch (condition) {
      case 'Maintained': return 'bg-green-900 text-green-200';
      case 'Neglected': return 'bg-yellow-900 text-yellow-200';
      case 'Compromised': return 'bg-red-900 text-red-200';
      default: return 'bg-gray-900 text-gray-200';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Followers</h2>
        <div className="text-sm text-gray-400">
          {followers.length} follower{followers.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Add New Follower Form */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Add New Follower</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-12">
          <div className="sm:col-span-5">
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Follower Name
            </label>
            <input
              type="text"
              value={newFollower.name}
              onChange={(e) => setNewFollower(prev => ({ ...prev, name: e.target.value }))}
              className="input-field w-full"
              placeholder="e.g., Apprentice, Bodyguard, Informant"
            />
          </div>
          <div className="sm:col-span-3">
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Capability
            </label>
            <select
              value={newFollower.cap}
              onChange={(e) => setNewFollower(prev => ({ ...prev, cap: parseInt(e.target.value) }))}
              className="input-field w-full"
            >
              {[1, 2, 3, 4, 5, 6].map(num => (
                <option key={num} value={num}>Cap {num}</option>
              ))}
            </select>
          </div>
          <div className="sm:col-span-3">
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Condition
            </label>
            <select
              value={newFollower.condition}
              onChange={(e) => setNewFollower(prev => ({ ...prev, condition: e.target.value }))}
              className="input-field w-full"
            >
              {conditions.map(condition => (
                <option key={condition} value={condition}>{condition}</option>
              ))}
            </select>
          </div>
          <div className="sm:col-span-1 flex items-end">
            <button
              onClick={handleAddFollower}
              disabled={isSaving || !newFollower.name.trim()}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Add
            </button>
          </div>
        </div>
      </div>

      {/* Followers List */}
      {followers.length > 0 ? (
        <div className="bg-gray-700 rounded-lg overflow-hidden">
          <ul className="divide-y divide-gray-600">
            {followers.map((follower, index) => (
              <li key={index} className="px-6 py-4">
                {editingIndex === index ? (
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-12 items-center">
                    <div className="sm:col-span-5">
                      <input
                        type="text"
                        value={editFollower.name}
                        onChange={(e) => setEditFollower(prev => ({ ...prev, name: e.target.value }))}
                        className="input-field w-full"
                      />
                    </div>
                    <div className="sm:col-span-3">
                      <select
                        value={editFollower.cap}
                        onChange={(e) => setEditFollower(prev => ({ ...prev, cap: parseInt(e.target.value) }))}
                        className="input-field w-full"
                      >
                        {[1, 2, 3, 4, 5, 6].map(num => (
                          <option key={num} value={num}>Cap {num}</option>
                        ))}
                      </select>
                    </div>
                    <div className="sm:col-span-3">
                      <select
                        value={editFollower.condition}
                        onChange={(e) => setEditFollower(prev => ({ ...prev, condition: e.target.value }))}
                        className="input-field w-full"
                      >
                        {conditions.map(condition => (
                          <option key={condition} value={condition}>{condition}</option>
                        ))}
                      </select>
                    </div>
                    <div className="sm:col-span-1 flex space-x-2">
                      <button
                        onClick={handleSaveEdit}
                        disabled={isSaving || !editFollower.name.trim()}
                        className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => setEditingIndex(null)}
                        className="btn-secondary"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <span className="text-white font-medium">{follower.name}</span>
                      <span className="ml-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-900 text-purple-200">
                        Cap {follower.cap}
                      </span>
                      <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getConditionColor(follower.condition)}`}>
                        {follower.condition}
                      </span>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEditFollower(index)}
                        className="p-2 rounded-full bg-gray-600 text-gray-300 hover:bg-gray-500"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteFollower(index)}
                        disabled={isSaving}
                        className="p-2 rounded-full bg-red-900 text-red-300 hover:bg-red-800 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <div className="bg-gray-700 rounded-lg p-12 text-center">
          <PlusIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-200">No followers</h3>
          <p className="mt-1 text-sm text-gray-400">
            Add your first follower using the form above.
          </p>
        </div>
      )}

      {/* Followers Guide */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Follower Information</h3>
        <div className="prose prose-invert max-w-none text-gray-300">
          <p className="mb-3">
            Followers are NPCs who assist your character. They can be allies, servants, contacts, or companions.
          </p>
          <p className="mb-3">
            <strong>Capability (Cap):</strong> Represents the follower's effectiveness (1-6).
          </p>
          <p className="mb-3">
            <strong>Conditions:</strong>
          </p>
          <ul className="list-disc list-inside space-y-1 mb-3">
            <li><span className="text-green-200">Maintained</span> - Loyal and effective</li>
            <li><span className="text-yellow-200">Neglected</span> - May require attention</li>
            <li><span className="text-red-200">Compromised</span> - Loyalty or effectiveness is questionable</li>
          </ul>
          <p>
            Followers can be activated during scenes to provide assistance, but their condition affects their reliability.
          </p>
        </div>
      </div>
    </div>
  );
};

export default FollowersTab;

