// frontend/src/components/macros/MacroManager.jsx (updated)
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useMacroStore } from '../../store/macroStore';
import { useCampaignStore } from '../../store/campaignStore';
import { useAuthStore } from '../../store/authStore';
import MacroList from './MacroList';
import MacroForm from './MacroForm';

const MacroManager = () => {
  const { id: campaignId } = useParams();
  const { macros, getCampaignMacros, isLoading, error } = useMacroStore();
  const { currentCampaign } = useCampaignStore();
  const { user } = useAuthStore();
  const [showForm, setShowForm] = useState(false);
  const [editingMacro, setEditingMacro] = useState(null);

  useEffect(() => {
    if (campaignId) {
      getCampaignMacros(campaignId);
    }
  }, [campaignId, getCampaignMacros]);

  const isGM = currentCampaign?.gmuserid === user?.userid;

  const handleEdit = (macro) => {
    setEditingMacro(macro);
    setShowForm(true);
  };

  const handleCreate = () => {
    setEditingMacro(null);
    setShowForm(true);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingMacro(null);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-fate-accent">Loading macros...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-900/50 border border-red-700 rounded-lg p-4">
          <h3 className="text-red-300 font-medium">Error loading macros</h3>
          <p className="text-red-200 mt-1">{error}</p>
          <button
            onClick={() => getCampaignMacros(campaignId)}
            className="mt-3 btn-primary"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-fate-accent">Campaign Macros</h1>
        {isGM && (
          <button
            onClick={handleCreate}
            className="btn-primary"
          >
            Create Macro
          </button>
        )}
      </div>

      {showForm ? (
        <MacroForm
          campaignId={campaignId}
          macro={editingMacro}
          onCancel={handleCancel}
          isGM={isGM}
        />
      ) : (
        <MacroList
          macros={macros}
          onEdit={handleEdit}
          isGM={isGM}
          campaignId={campaignId}
        />
      )}
    </div>
  );
};

export default MacroManager;

