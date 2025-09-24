import React from 'react';
import { DiceIcon } from '@heroicons/react/24/outline';

const DiceDisplay = ({ roll, isRolling }) => {
  if (isRolling) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="flex space-x-2 mb-4">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center animate-bounce"
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <span className="text-white font-bold text-lg">?</span>
            </div>
          ))}
        </div>
        <p className="text-gray-400">Rolling...</p>
      </div>
    );
  }

  if (!roll) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <DiceIcon className="h-16 w-16 text-gray-600 mb-4" />
        <h3 className="text-lg font-medium text-gray-400">No roll yet</h3>
        <p className="text-sm text-gray-500 mt-1">
          Configure your roll and click "Roll Dice"
        </p>
      </div>
    );
  }

  const getDiceColor = (value) => {
    if (value === 1) return 'bg-red-600 border-red-700'; // Complication
    if (value >= 6) return 'bg-green-600 border-green-700'; // Success
    return 'bg-gray-600 border-gray-700'; // Failure
  };

  const getResultColor = (description) => {
    if (description.includes('Exceptional') || description.includes('Major')) {
      return 'text-green-400';
    }
    if (description.includes('Moderate') || description.includes('Marginal')) {
      return 'text-yellow-400';
    }
    if (description.includes('Failure')) {
      return 'text-red-400';
    }
    return 'text-gray-400';
  };

  return (
    <div className="space-y-6">
      {/* Roll Summary */}
      <div className="text-center">
        <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-900 text-purple-200 mb-2">
          {roll.descriptionLevel} Roll
        </div>
        <h3 className={`text-2xl font-bold ${getResultColor(roll.description)}`}>
          {roll.description}
        </h3>
        <p className="text-gray-400 mt-1">
          {roll.successes} Success{roll.successes !== 1 ? 'es' : ''} • 
          {roll.complications} Complication{roll.complications !== 1 ? 's' : ''}
        </p>
        {roll.notes && (
          <p className="text-sm text-gray-500 mt-2 italic">
            "{roll.notes}"
          </p>
        )}
      </div>

      {/* Dice Display */}
      <div className="flex flex-wrap justify-center gap-2">
        {roll.dice.map((die, index) => (
          <div
            key={index}
            className={`w-12 h-12 ${getDiceColor(die)} border-2 rounded-lg flex items-center justify-center transform hover:scale-110 transition-transform duration-200`}
          >
            <span className="text-white font-bold text-lg">{die}</span>
          </div>
        ))}
      </div>

      {/* Pool Information */}
      <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-700">
        <div className="text-center">
          <p className="text-sm text-gray-400">Dice Pool</p>
          <p className="text-xl font-bold text-white">{roll.pool}</p>
        </div>
        <div className="text-center">
          <p className="text-sm text-gray-400">Roll ID</p>
          <p className="text-sm font-mono text-gray-400">
            {roll.rollId?.substring(0, 8) || 'N/A'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default DiceDisplay;

