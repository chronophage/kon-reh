import React, { useState } from 'react';
import { ArrowPathIcon } from '@heroicons/react/24/outline';

const RollControls = ({ characters, onRoll, onDrawComplications, isRolling }) => {
  const [pool, setPool] = useState(4);
  const [descriptionLevel, setDescriptionLevel] = useState('Basic');
  const [selectedCharacter, setSelectedCharacter] = useState('');
  const [notes, setNotes] = useState('');

  const descriptionLevels = [
    { id: 'Basic', name: 'Basic', description: 'Standard roll' },
    { id: 'Detailed', name: 'Detailed', description: 'Re-roll one complication' },
    { id: 'Intricate', name: 'Intricate', description: 'Re-roll all complications' }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const rollConfig = {
      pool: parseInt(pool),
      descriptionLevel,
      notes: notes.trim() || undefined
    };

    if (selectedCharacter) {
      rollConfig.characterId = selectedCharacter;
    }

    onRoll(rollConfig);
  };

  const handleQuickRoll = (diceCount) => {
    setPool(diceCount);
    setDescriptionLevel('Basic');
    setNotes(`Quick ${diceCount}d10 roll`);
    
    const rollConfig = {
      pool: diceCount,
      descriptionLevel: 'Basic',
      notes: `Quick ${diceCount}d10 roll`
    };

    if (selectedCharacter) {
      rollConfig.characterId = selectedCharacter;
    }

    onRoll(rollConfig);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Character Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Character (Optional)
        </label>
        <select
          value={selectedCharacter}
          onChange={(e) => setSelectedCharacter(e.target.value)}
          className="input-field w-full"
        >
          <option value="">No character</option>
          {characters.map(character => (
            <option key={character.characterid} value={character.characterid}>
              {character.name}
            </option>
          ))}
        </select>
      </div>

      {/* Dice Pool */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Dice Pool ({pool} dice)
        </label>
        <input
          type="range"
          min="1"
          max="20"
          value={pool}
          onChange={(e) => setPool(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
          disabled={isRolling}
        />
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>1</span>
          <span>10</span>
          <span>20</span>
        </div>
      </div>

      {/* Description Level */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Description Level
        </label>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
          {descriptionLevels.map((level) => (
            <button
              key={level.id}
              type="button"
              onClick={() => setDescriptionLevel(level.id)}
              className={`p-3 rounded-lg border text-left transition-colors duration-200 ${
                descriptionLevel === level.id
                  ? 'border-purple-500 bg-purple-900/50 text-white'
                  : 'border-gray-600 bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
              disabled={isRolling}
            >
              <div className="font-medium">{level.name}</div>
              <div className="text-xs mt-1">{level.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Notes */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Notes (Optional)
        </label>
        <input
          type="text"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          className="input-field w-full"
          placeholder="e.g., Climbing the wall, Spell casting..."
          disabled={isRolling}
        />
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-3">
        <button
          type="submit"
          disabled={isRolling}
          className="btn-primary flex items-center justify-center flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isRolling ? (
            <>
              <ArrowPathIcon className="h-4 w-4 mr-2 animate-spin" />
              Rolling...
            </>
          ) : (
            'Roll Dice'
          )}
        </button>
        
        <button
          type="button"
          onClick={() => {
            setPool(4);
            setDescriptionLevel('Basic');
            setNotes('');
            setSelectedCharacter('');
          }}
          className="btn-secondary flex-1"
          disabled={isRolling}
        >
          Reset
        </button>
      </div>

      {/* Quick Roll Buttons */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Quick Rolls
        </label>
        <div className="grid grid-cols-4 gap-2">
          {[2, 4, 6, 8].map((count) => (
            <button
              key={count}
              type="button"
              onClick={() => handleQuickRoll(count)}
              disabled={isRolling}
              className="py-2 px-3 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {count}d10
            </button>
          ))}
        </div>
      </div>
    </form>
  );
};

export default RollControls;

