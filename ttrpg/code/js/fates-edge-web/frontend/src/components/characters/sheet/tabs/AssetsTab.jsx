import React, { useState } from 'react';
import { useCharacterStore } from '../../../../store/characterStore';
import { PlusIcon, TrashIcon, PencilIcon } from '@heroicons/react/24/outline';

const AssetsTab = ({ character }) => {
  const { updateCharacter } = useCharacterStore();
  const [assets, setAssets] = useState(character.assets || []);
  const [newAsset, setNewAsset] = useState({ name: '', tier: 1, condition: 'Maintained' });
  const [editingIndex, setEditingIndex] = useState(null);
  const [editAsset, setEditAsset] = useState({ name: '', tier: 1, condition: 'Maintained' });
  const [isSaving, setIsSaving] = useState(false);

  const conditions = ['Maintained', 'Neglected', 'Compromised'];

  const handleAddAsset = async () => {
    if (!newAsset.name.trim()) return;
    
    const updatedAssets = [...assets, newAsset];
    setAssets(updatedAssets);
    setNewAsset({ name: '', tier: 1, condition: 'Maintained' });
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { assets: updatedAssets });
    } catch (error) {
      console.error('Failed to add asset:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleEditAsset = (index) => {
    setEditingIndex(index);
    setEditAsset({ ...assets[index] });
  };

  const handleSaveEdit = async () => {
    if (!editAsset.name.trim()) return;
    
    const updatedAssets = [...assets];
    updatedAssets[editingIndex] = editAsset;
    setAssets(updatedAssets);
    setEditingIndex(null);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { assets: updatedAssets });
    } catch (error) {
      console.error('Failed to update asset:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteAsset = async (index) => {
    const updatedAssets = assets.filter((_, i) => i !== index);
    setAssets(updatedAssets);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { assets: updatedAssets });
    } catch (error) {
      console.error('Failed to delete asset:', error);
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
        <h2 className="text-xl font-bold text-white">Assets</h2>
        <div className="text-sm text-gray-400">
          {assets.length} asset{assets.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Add New Asset Form */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Add New Asset</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-12">
          <div className="sm:col-span-5">
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Asset Name
            </label>
            <input
              type="text"
              value={newAsset.name}
              onChange={(e) => setNewAsset(prev => ({ ...prev, name: e.target.value }))}
              className="input-field w-full"
              placeholder="e.g., Magic Sword, Safehouse, Wealth"
            />
          </div>
          <div className="sm:col-span-3">
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Tier
            </label>
            <select
              value={newAsset.tier}
              onChange={(e) => setNewAsset(prev => ({ ...prev, tier: parseInt(e.target.value) }))}
              className="input-field w-full"
            >
              {[1, 2, 3, 4, 5, 6].map(num => (
                <option key={num} value={num}>Tier {num}</option>
              ))}
            </select>
          </div>
          <div className="sm:col-span-3">
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Condition
            </label>
            <select
              value={newAsset.condition}
              onChange={(e) => setNewAsset(prev => ({ ...prev, condition: e.target.value }))}
              className="input-field w-full"
            >
              {conditions.map(condition => (
                <option key={condition} value={condition}>{condition}</option>
              ))}
            </select>
          </div>
          <div className="sm:col-span-1 flex items-end">
            <button
              onClick={handleAddAsset}
              disabled={isSaving || !newAsset.name.trim()}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Add
            </button>
          </div>
        </div>
      </div>

      {/* Assets List */}
      {assets.length > 0 ? (
        <div className="bg-gray-700 rounded-lg overflow-hidden">
          <ul className="divide-y divide-gray-600">
            {assets.map((asset, index) => (
              <li key={index} className="px-6 py-4">
                {editingIndex === index ? (
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-12 items-center">
                    <div className="sm:col-span-5">
                      <input
                        type="text"
                        value={editAsset.name}
                        onChange={(e) => setEditAsset(prev => ({ ...prev, name: e.target.value }))}
                        className="input-field w-full"
                      />
                    </div>
                    <div className="sm:col-span-3">
                      <select
                        value={editAsset.tier}
                        onChange={(e) => setEditAsset(prev => ({ ...prev, tier: parseInt(e.target.value) }))}
                        className="input-field w-full"
                      >
                        {[1, 2, 3, 4, 5, 6].map(num => (
                          <option key={num} value={num}>Tier {num}</option>
                        ))}
                      </select>
                    </div>
                    <div className="sm:col-span-3">
                      <select
                        value={editAsset.condition}
                        onChange={(e) => setEditAsset(prev => ({ ...prev, condition: e.target.value }))}
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
                        disabled={isSaving || !editAsset.name.trim()}
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
                      <span className="text-white font-medium">{asset.name}</span>
                      <span className="ml-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-900 text-purple-200">
                        Tier {asset.tier}
                      </span>
                      <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getConditionColor(asset.condition)}`}>
                        {asset.condition}
                      </span>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEditAsset(index)}
                        className="p-2 rounded-full bg-gray-600 text-gray-300 hover:bg-gray-500"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteAsset(index)}
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
          <h3 className="mt-2 text-sm font-medium text-gray-200">No assets</h3>
          <p className="mt-1 text-sm text-gray-400">
            Add your first asset using the form above.
          </p>
        </div>
      )}

      {/* Assets Guide */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Asset Conditions</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div>
            <h4 className="font-medium text-green-200">Maintained</h4>
            <p className="mt-1 text-sm text-gray-400">
              Asset is in perfect working condition and provides full benefits.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-yellow-200">Neglected</h4>
            <p className="mt-1 text-sm text-gray-400">
              Asset has been ignored and may require attention. Reduced effectiveness.
            </p>
          </div>
          <div>
            <h4 className="font-medium text-red-200">Compromised</h4>
            <p className="mt-1 text-sm text-gray-400">
              Asset is damaged or threatened. May fail when needed most.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssetsTab;

