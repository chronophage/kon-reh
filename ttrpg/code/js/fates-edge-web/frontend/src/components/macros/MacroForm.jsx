// frontend/src/components/macros/MacroForm.jsx
import React, { useState } from 'react';
import { useMacroStore } from '../../store/macroStore';

const MacroForm = ({ campaignId, macro, onCancel, isGM }) => {
  const { createMacro, updateMacro, isLoading } = useMacroStore();
  const [formData, setFormData] = useState({
    name: macro?.name || '',
    command: macro?.command || '',
    description: macro?.description || '',
    isPublic: macro?.ispublic ?? true
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (macro) {
        await updateMacro(macro.macroid, formData);
      } else {
        await createMacro(campaignId, formData);
      }
      onCancel();
    } catch (error) {
      console.error('Failed to save macro:', error);
    }
  };

  return (
    <div className="bg-fate-dark rounded-lg p-6">
      <h2 className="text-xl font-bold text-fate-accent mb-6">
        {macro ? 'Edit Macro' : 'Create New Macro'}
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Macro Name *
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="input-field w-full"
            placeholder="Enter macro name"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Command *
          </label>
          <div className="relative">
            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-fate-accent">
              /
            </span>
            <input
              type="text"
              name="command"
              value={formData.command}
              onChange={handleChange}
              required
              className="input-field w-full pl-8"
              placeholder="Enter command (e.g., roll, xp, etc.)"
            />
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Players will type /{formData.command} to use this macro
          </p>
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
            placeholder="Describe what this macro does"
          />
        </div>
        
        {isGM && (
          <div className="flex items-center">
            <input
              type="checkbox"
              name="isPublic"
              checked={formData.isPublic}
              onChange={handleChange}
              className="rounded bg-fate-dark border-fate-dark text-fate-accent focus:ring-fate-accent"
            />
            <label className="ml-2 text-sm text-gray-300">
              Make this macro available to all players
            </label>
          </div>
        )}
        
        <div className="flex justify-end space-x-4 pt-4">
          <button
            type="button"
            onClick={onCancel}
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
            {isLoading ? 'Saving...' : 'Save Macro'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default MacroForm;

