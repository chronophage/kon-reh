// frontend/src/components/characters/CharacterCreator.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCharacterStore } from '../../store/characterStore';

const CharacterCreator = () => {
  const navigate = useNavigate();
  const { createCharacter, isLoading, error } = useCharacterStore();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    species: '',
    background: '',
    archetype: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newCharacter = await createCharacter(formData);
      navigate(`/characters/${newCharacter.characterid}`);
    } catch (err) {
      console.error('Failed to create character:', err);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="bg-fate-dark rounded-lg p-6">
        <h1 className="text-2xl font-bold text-fate-accent mb-6">Create New Character</h1>
        
        {error && (
          <div className="bg-red-900/50 border border-red-700 rounded-lg p-4 mb-6">
            <p className="text-red-200">{error}</p>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Character Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="input-field w-full"
              placeholder="Enter character name"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              className="input-field w-full"
              placeholder="Describe your character"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Species
              </label>
              <input
                type="text"
                name="species"
                value={formData.species}
                onChange={handleChange}
                className="input-field w-full"
                placeholder="Character species"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Background
              </label>
              <input
                type="text"
                name="background"
                value={formData.background}
                onChange={handleChange}
                className="input-field w-full"
                placeholder="Character background"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Archetype
            </label>
            <input
              type="text"
              name="archetype"
              value={formData.archetype}
              onChange={handleChange}
              className="input-field w-full"
              placeholder="Character archetype"
            />
          </div>
          
          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={() => navigate('/characters')}
              className="px-4 py-2 border border-gray-600 rounded-lg text-gray-300 hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary flex items-center"
            >
              {isLoading && (
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              )}
              {isLoading ? 'Creating...' : 'Create Character'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CharacterCreator;

