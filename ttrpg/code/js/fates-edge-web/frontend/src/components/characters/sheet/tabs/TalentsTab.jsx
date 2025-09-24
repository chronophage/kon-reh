import React, { useState } from 'react';
import { useCharacterStore } from '../../../../store/characterStore';
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline';

const TalentsTab = ({ character }) => {
  const { updateCharacter } = useCharacterStore();
  const [talents, setTalents] = useState(character.talents || []);
  const [newTalent, setNewTalent] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  const handleAddTalent = async () => {
    if (!newTalent.trim()) return;
    
    const updatedTalents = [...talents, newTalent.trim()];
    setTalents(updatedTalents);
    setNewTalent('');
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { talents: updatedTalents });
    } catch (error) {
      console.error('Failed to add talent:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteTalent = async (index) => {
    const updatedTalents = talents.filter((_, i) => i !== index);
    setTalents(updatedTalents);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { talents: updatedTalents });
    } catch (error) {
      console.error('Failed to delete talent:', error);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Talents</h2>
        <div className="text-sm text-gray-400">
          {talents.length} talent{talents.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Add New Talent Form */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Add New Talent</h3>
        <div className="flex space-x-4">
          <div className="flex-1">
            <input
              type="text"
              value={newTalent}
              onChange={(e) => setNewTalent(e.target.value)}
              className="input-field w-full"
              placeholder="e.g., Spellcasting, Combat Reflexes, Socialite"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={handleAddTalent}
              disabled={isSaving || !newTalent.trim()}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSaving ? 'Adding...' : 'Add Talent'}
            </button>
          </div>
        </div>
      </div>

      {/* Talents List */}
      {talents.length > 0 ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {talents.map((talent, index) => (
            <div key={index} className="bg-gray-700 rounded-lg p-4 flex items-center justify-between">
              <span className="text-white font-medium">{talent}</span>
              <button
                onClick={() => handleDeleteTalent(index)}
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
          <h3 className="mt-2 text-sm font-medium text-gray-200">No talents</h3>
          <p className="mt-1 text-sm text-gray-400">
            Add your first talent using the form above.
          </p>
        </div>
      )}

      {/* Talents Guide */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">About Talents</h3>
        <div className="prose prose-invert max-w-none text-gray-300">
          <p className="mb-3">
            Talents represent special abilities, unique skills, or exceptional traits that set your character apart. 
            They can be supernatural powers, combat techniques, social advantages, or any other distinctive capability.
          </p>
          <p className="mb-3">
            Examples include:
          </p>
          <ul className="list-disc list-inside space-y-1 mb-3">
            <li>Spellcasting - Ability to cast arcane spells</li>
            <li>Combat Reflexes - Enhanced reaction time in battle</li>
            <li>Socialite - Exceptional ability to influence others</li>
            <li>Keen Senses - Superior perception and awareness</li>
            <li>Iron Will - Resistance to mental effects</li>
          </ul>
          <p>
            Talents should be specific and meaningful to your character's concept and the campaign setting.
          </p>
        </div>
      </div>
    </div>
  );
};

export default TalentsTab;

