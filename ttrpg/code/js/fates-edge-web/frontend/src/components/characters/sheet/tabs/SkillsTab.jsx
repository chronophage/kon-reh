import React, { useState } from 'react';
import { useCharacterStore } from '../../../../store/characterStore';
import { PlusIcon, TrashIcon, PencilIcon } from '@heroicons/react/24/outline';

const SkillsTab = ({ character }) => {
  const { updateCharacter } = useCharacterStore();
  const [skills, setSkills] = useState(character.skills || []);
  const [newSkill, setNewSkill] = useState({ name: '', rating: 1 });
  const [editingIndex, setEditingIndex] = useState(null);
  const [editSkill, setEditSkill] = useState({ name: '', rating: 1 });
  const [isSaving, setIsSaving] = useState(false);

  const handleAddSkill = async () => {
    if (!newSkill.name.trim()) return;
    
    const updatedSkills = [...skills, newSkill];
    setSkills(updatedSkills);
    setNewSkill({ name: '', rating: 1 });
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { skills: updatedSkills });
    } catch (error) {
      console.error('Failed to add skill:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleEditSkill = (index) => {
    setEditingIndex(index);
    setEditSkill({ ...skills[index] });
  };

  const handleSaveEdit = async () => {
    if (!editSkill.name.trim()) return;
    
    const updatedSkills = [...skills];
    updatedSkills[editingIndex] = editSkill;
    setSkills(updatedSkills);
    setEditingIndex(null);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { skills: updatedSkills });
    } catch (error) {
      console.error('Failed to update skill:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteSkill = async (index) => {
    const updatedSkills = skills.filter((_, i) => i !== index);
    setSkills(updatedSkills);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { skills: updatedSkills });
    } catch (error) {
      console.error('Failed to delete skill:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleRatingChange = (value, isEdit = false) => {
    const setValue = isEdit ? setEditSkill : setNewSkill;
    setValue(prev => ({ ...prev, rating: Math.max(1, Math.min(6, value)) }));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Skills</h2>
        <div className="text-sm text-gray-400">
          {skills.length} skill{skills.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Add New Skill Form */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Add New Skill</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Skill Name
            </label>
            <input
              type="text"
              value={newSkill.name}
              onChange={(e) => setNewSkill(prev => ({ ...prev, name: e.target.value }))}
              className="input-field"
              placeholder="e.g., Melee, Stealth, Lore"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Rating
            </label>
            <select
              value={newSkill.rating}
              onChange={(e) => handleRatingChange(parseInt(e.target.value))}
              className="input-field"
            >
              {[1, 2, 3, 4, 5, 6].map(num => (
                <option key={num} value={num}>{num}</option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={handleAddSkill}
              disabled={isSaving || !newSkill.name.trim()}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSaving ? 'Adding...' : 'Add Skill'}
            </button>
          </div>
        </div>
      </div>

      {/* Skills List */}
      {skills.length > 0 ? (
        <div className="bg-gray-700 rounded-lg overflow-hidden">
          <ul className="divide-y divide-gray-600">
            {skills.map((skill, index) => (
              <li key={index} className="px-6 py-4">
                {editingIndex === index ? (
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-12 items-center">
                    <div className="sm:col-span-6">
                      <input
                        type="text"
                        value={editSkill.name}
                        onChange={(e) => setEditSkill(prev => ({ ...prev, name: e.target.value }))}
                        className="input-field w-full"
                      />
                    </div>
                    <div className="sm:col-span-3">
                      <select
                        value={editSkill.rating}
                        onChange={(e) => handleRatingChange(parseInt(e.target.value), true)}
                        className="input-field w-full"
                      >
                        {[1, 2, 3, 4, 5, 6].map(num => (
                          <option key={num} value={num}>{num}</option>
                        ))}
                      </select>
                    </div>
                    <div className="sm:col-span-3 flex space-x-2">
                      <button
                        onClick={handleSaveEdit}
                        disabled={isSaving || !editSkill.name.trim()}
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
                      <span className="text-lg font-medium text-white">{skill.name}</span>
                      <span className="ml-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-900 text-purple-200">
                        {skill.rating}
                      </span>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEditSkill(index)}
                        className="p-2 rounded-full bg-gray-600 text-gray-300 hover:bg-gray-500"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteSkill(index)}
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
          <h3 className="mt-2 text-sm font-medium text-gray-200">No skills</h3>
          <p className="mt-1 text-sm text-gray-400">
            Add your first skill using the form above.
          </p>
        </div>
      )}

      {/* Skill Ratings Guide */}
      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Skill Ratings Guide</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div>
            <h4 className="font-medium text-gray-300">1 - Novice</h4>
            <p className="mt-1 text-sm text-gray-400">Basic familiarity with the skill</p>
          </div>
          <div>
            <h4 className="font-medium text-gray-300">2-3 - Competent</h4>
            <p className="mt-1 text-sm text-gray-400">Reliable ability in most situations</p>
          </div>
          <div>
            <h4 className="font-medium text-gray-300">4-6 - Expert</h4>
            <p className="mt-1 text-sm text-gray-400">Exceptional mastery of the skill</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SkillsTab;

