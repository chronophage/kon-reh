import React, { useState } from 'react';
import { useCharacterStore } from '../../../../store/characterStore';
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline';

const ComplicationsTab = ({ character }) => {
  const { updateCharacter } = useCharacterStore();
  const [complications, setComplications] = useState(character.complications || []);
  const [newComplication, setNewComplication] = useState('');
  const [boons, setBoons] = useState(character.boons || 0);
  const [isSaving, setIsSaving] = useState(false);

  const handleAddComplication = async () => {
    if (!newComplication.trim()) return;
    
    const updatedComplications = [...complications, newComplication.trim()];
    setComplications(updatedComplications);
    setNewComplication('');
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { 
        complications: updatedComplications 
      });
    } catch (error) {
      console.error('Failed to add complication:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteComplication = async (index) => {
    const updatedComplications = complications.filter((_, i) => i !== index);
    setComplications(updatedComplications);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { 
        complications: updatedComplications 
      });
    } catch (error) {
      console.error('Failed to delete complication:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleSpendBoon = async () => {
    if (boons <= 0) return;
    
    const newBoons = boons - 1;
    setBoons(newBoons);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { boons: newBoons });
    } catch (error) {
      console.error('Failed to spend boon:', error);
      setBoons(boons); // Revert on error
    } finally {
      setIsSaving(false);
    }
  };

  const handleConvertBoon = async () => {
    if (boons <= 0) return;
    
    const newBoons = boons - 1;
    const newXpTotal = character.xptotal + 2;
    
    setBoons(newBoons);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { 
        boons: newBoons,
        xptotal: newXpTotal
      });
    } catch (error) {
      console.error('Failed to convert boon:', error);
      setBoons(boons); // Revert on error
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Complications & Boons</h2>
        <div className="flex items-center space-x-4">
          <div className="text-sm text-gray-400">
            {complications.length} complication{complications.length !== 1 ? 's' : ''}
          </div>
          <div className="flex items-center">
            <span className="text-sm text-gray-400 mr-2">Boons:</span>
            <span className="text-lg font-bold text-purple-400">{boons}</span>
          </div>
        </div>
      </div>

      {/* Boons Management */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Boon Management</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="bg-gray-800 rounded-lg p-4">
            <h4 className="font-medium text-gray-300 mb-2">Spend Boon</h4>
            <p className="text-sm text-gray-400 mb-3">
              Use a boon to activate an asset or gain a narrative advantage.
            </p>
            <button
              onClick={handleSpendBoon}
              disabled={isSaving || boons <= 0}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSaving ? 'Processing...' : `Spend 1 Boon (${boons} remaining)`}
            </button>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <h4 className="font-medium text-gray-300 mb-2">Convert to XP</h4>
            <p className="text-sm text-gray-400 mb-3">
              Convert 1 boon to 2 XP for character advancement.
            </p>
            <button
              onClick={handleConvertBoon}
              disabled={isSaving || boons <= 0}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSaving ? 'Processing...' : `Convert 1 Boon to 2 XP`}
            </button>
          </div>
        </div>
      </div>

      {/* Add New Complication Form */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Add New Complication</h3>
        <div className="flex space-x-4">
          <div className="flex-1">
            <input
              type="text"
              value={newComplication}
              onChange={(e) => setNewComplication(e.target.value)}
              className="input-field w-full"
              placeholder="e.g., Enemy, Secret, Debt, Addiction"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={handleAddComplication}
              disabled={isSaving || !newComplication.trim()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSaving ? 'Adding...' : 'Add Complication'}
            </button>
          </div>
        </div>
      </div>

      {/* Complications List */}
      {complications.length > 0 ? (
        <div className="grid grid-cols-1 gap-4">
          {complications.map((complication, index) => (
            <div key={index} className="bg-gray-700 rounded-lg p-4 flex items-center justify-between">
              <div className="flex items-center">
                <div className="flex-shrink-0 h-6 w-6 rounded-full bg-red-900 flex items-center justify-center">
                  <span className="text-red-200 text-xs font-bold">!</span>
                </div>
                <span className="ml-3 text-white font-medium">{complication}</span>
              </div>
              <button
                onClick={() => handleDeleteComplication(index)}
                disabled={isSaving}
                className="p-1 rounded-full bg-red-900 text-red-300 hover:bg-red-800 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <TrashIcon className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-gray-700 rounded-lg p-12 text-center">
          <PlusIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-200">No complications</h3>
          <p className="mt-1 text-sm text-gray-400">
            Add your first complication using the form above.
          </p>
        </div>
      )}

      {/* Complications Guide */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">About Complications</h3>
        <div className="prose prose-invert max-w-none text-gray-300">
          <p className="mb-3">
            Complications are narrative elements that create tension and drive the story forward. 
            They represent ongoing challenges, secrets, enemies, or other factors that complicate your character's life.
          </p>
          <p className="mb-3">
            <strong>Benefits of Complications:</strong>
          </p>
          <ul className="list-disc list-inside space-y-1 mb-3">
            <li>Earn boons when you embrace complications during play</li>
            <li>Provide rich storytelling opportunities</li>
            <li>Deepen character development and motivation</li>
            <li>Create meaningful consequences for character actions</li>
          </ul>
          <p className="mb-3">
            <strong>Examples:</strong>
          </p>
          <ul className="list-disc list-inside space-y-1">
            <li><strong>Enemy:</strong> A persistent foe who seeks to harm you</li>
            <li><strong>Secret:</strong> A hidden truth that could destroy you if revealed</li>
            <li><strong>Debt:</strong> Financial or moral obligation to another party</li>
            <li><strong>Addiction:</strong> Dependence on a substance or behavior</li>
            <li><strong>Duty:</strong> Obligation to an organization or cause</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ComplicationsTab;

