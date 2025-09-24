import React, { useState, useEffect } from 'react';
import { useMacroStore } from '../../store/macroStore';
import { XMarkIcon, PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';

const MacroPanel = ({ campaignId, isGM, onClose }) => {
  const { 
    macros, 
    pendingMacros, 
    isLoading, 
    getCampaignMacros, 
    getPendingMacros, 
    createMacro, 
    updateMacro, 
    deleteMacro, 
    approveMacro 
  } = useMacroStore();
  
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingMacro, setEditingMacro] = useState(null);
  const [newMacro, setNewMacro] = useState({
    name: '',
    command: '',
    description: '',
    isPublic: false
  });

  useEffect(() => {
    const fetchData = async () => {
      await getCampaignMacros(campaignId);
      if (isGM) {
        await getPendingMacros(campaignId);
      }
    };

    fetchData();
  }, [campaignId, getCampaignMacros, getPendingMacros, isGM]);

  const handleCreateMacro = async (e) => {
    e.preventDefault();
    try {
      await createMacro({
        campaignId,
        ...newMacro
      });
      setNewMacro({ name: '', command: '', description: '', isPublic: false });
      setShowCreateForm(false);
    } catch (error) {
      console.error('Failed to create macro:', error);
    }
  };

  const handleUpdateMacro = async (e) => {
    e.preventDefault();
    try {
      await updateMacro(editingMacro.macroid, editingMacro);
      setEditingMacro(null);
    } catch (error) {
      console.error('Failed to update macro:', error);
    }
  };

  const handleDeleteMacro = async (macroId, name) => {
    if (window.confirm(`Are you sure you want to delete the macro "${name}"?`)) {
      try {
        await deleteMacro(macroId);
      } catch (error) {
        console.error('Failed to delete macro:', error);
      }
    }
  };

  const handleApproveMacro = async (macroId) => {
    try {
      await approveMacro(macroId);
    } catch (error) {
      console.error('Failed to approve macro:', error);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-800">
      <div className="flex items-center justify-between p-4 border-b border-gray-700">
        <h3 className="text-lg font-medium text-white">Macros</h3>
        <button
          onClick={onClose}
          className="p-1 rounded-full bg-gray-700 text-gray-400 hover:bg-gray-600 md:hidden"
        >
          <XMarkIcon className="h-5 w-5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {isLoading ? (
          <div className="flex justify-center py-8">
            <svg className="animate-spin h-8 w-8 text-purple-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        ) : (
          <>
            {/* Create Macro Form */}
            {showCreateForm && (
              <div className="bg-gray-700 rounded-lg p-4 mb-4">
                <h4 className="text-md font-medium text-white mb-3">
                  {editingMacro ? 'Edit Macro' : 'Create New Macro'}
                </h4>
                <form onSubmit={editingMacro ? handleUpdateMacro : handleCreateMacro}>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-1">
                        Name
                      </label>
                      <input
                        type="text"
                        value={editingMacro ? editingMacro.name : newMacro.name}
                        onChange={(e) => 
                          editingMacro 
                            ? setEditingMacro({...editingMacro, name: e.target.value})
                            : setNewMacro({...newMacro, name: e.target.value})
                        }
                        className="input-field w-full text-sm"
                        placeholder="e.g., Fireball"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-1">
                        Command
                      </label>
                      <input
                        type="text"
                        value={editingMacro ? editingMacro.command : newMacro.command}
                        onChange={(e) => 
                          editingMacro 
                            ? setEditingMacro({...editingMacro, command: e.target.value})
                            : setNewMacro({...newMacro, command: e.target.value})
                        }
                        className="input-field w-full text-sm font-mono"
                        placeholder="e.g., !roll Wits + Arcana 4"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-1">
                        Description
                      </label>
                      <input
                        type="text"
                        value={editingMacro ? editingMacro.description : newMacro.description}
                        onChange={(e) => 
                          editingMacro 
                            ? setEditingMacro({...editingMacro, description: e.target.value})
                            : setNewMacro({...newMacro, description: e.target.value})
                        }
                        className="input-field w-full text-sm"
                        placeholder="Brief description of what this macro does"
                      />
                    </div>
                    {!editingMacro && (
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          id="isPublic"
                          checked={newMacro.isPublic}
                          onChange={(e) => setNewMacro({...newMacro, isPublic: e.target.checked})}
                          className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-600 rounded bg-gray-700"
                        />
                        <label htmlFor="isPublic" className="ml-2 block text-sm text-gray-300">
                          Make public (no approval needed)
                        </label>
                      </div>
                    )}
                  </div>
                  <div className="flex space-x-2 mt-4">
                    <button
                      type="submit"
                      className="btn-primary flex-1 text-sm"
                    >
                      {editingMacro ? 'Update' : 'Create'}
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setShowCreateForm(false);
                        setEditingMacro(null);
                      }}
                      className="btn-secondary flex-1 text-sm"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            )}

            {/* Pending Macros (GM only) */}
            {isGM && pendingMacros.length > 0 && (
              <div className="mb-6">
                <h4 className="text-md font-medium text-yellow-400 mb-3">
                  Pending Approval ({pendingMacros.length})
                </h4>
                <div className="space-y-2">
                  {pendingMacros.map(macro => (
                    <div key={macro.macroid} className="bg-yellow-900/50 rounded-lg p-3 border-l-4 border-yellow-500">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-yellow-200">{macro.name}</div>
                          <div className="text-sm font-mono text-yellow-300">{macro.command}</div>
                          <div className="text-xs text-yellow-400 mt-1">{macro.description}</div>
                          <div className="text-xs text-yellow-500 mt-1">
                            by {macro.creatorname}
                          </div>
                        </div>
                        <div className="flex space-x-1">
                          <button
                            onClick={() => handleApproveMacro(macro.macroid)}
                            className="p-1 rounded bg-green-600 text-white hover:bg-green-700"
                            title="Approve"
                          >
                            <PlusIcon className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleDeleteMacro(macro.macroid, macro.name)}
                            className="p-1 rounded bg-red-600 text-white hover:bg-red-700"
                            title="Reject"
                          >
                            <TrashIcon className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Approved Macros */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <h4 className="text-md font-medium text-white">
                  Approved Macros ({macros.length})
                </h4>
                <button
                  onClick={() => {
                    setShowCreateForm(true);
                    setEditingMacro(null);
                  }}
                  className="p-1 rounded-full bg-purple-600 text-white hover:bg-purple-700"
                  title="Create new macro"
                >
                  <PlusIcon className="h-4 w-4" />
                </button>
              </div>
              
              {macros.length > 0 ? (
                <div className="space-y-2">
                  {macros.map(macro => (
                    <div key={macro.macroid} className="bg-gray-700 rounded-lg p-3 hover:bg-gray-600">
                      <div className="flex items-center justify-between">
                        <div className="flex-1 min-w-0">
                          <div className="font-medium text-white truncate">{macro.name}</div>
                          <div className="text-sm font-mono text-purple-400 truncate">{macro.command}</div>
                          <div className="text-xs text-gray-400 mt-1 truncate">{macro.description}</div>
                          {macro.ispublic && (
                            <span className="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-green-900 text-green-200 mt-1">
                              Public
                            </span>
                          )}
                        </div>
                        <div className="flex space-x-1 ml-2">
                          <button
                            onClick={() => {
                              setEditingMacro(macro);
                              setShowCreateForm(true);
                            }}
                            className="p-1 rounded bg-gray-600 text-gray-300 hover:bg-gray-500"
                            title="Edit"
                          >
                            <PencilIcon className="h-3 w-3" />
                          </button>
                          <button
                            onClick={() => handleDeleteMacro(macro.macroid, macro.name)}
                            className="p-1 rounded bg-red-900 text-red-300 hover:bg-red-800"
                            title="Delete"
                          >
                            <TrashIcon className="h-3 w-3" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <CommandLineIcon className="h-12 w-12 mx-auto mb-3" />
                  <p>No macros yet</p>
                  <p className="text-sm mt-1">Create your first macro to get started</p>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

// Helper component for the icon
const CommandLineIcon = ({ className }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);

export default MacroPanel;

