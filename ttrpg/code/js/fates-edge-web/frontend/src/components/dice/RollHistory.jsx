import React from 'react';
import { useDiceStore } from '../../store/diceStore';
import { ClockIcon } from '@heroicons/react/24/outline';

const RollHistory = () => {
  const { rollHistory } = useDiceStore();

  const getResultEmoji = (description) => {
    if (description.includes('Exceptional') || description.includes('Major')) {
      return '🎉';
    }
    if (description.includes('Moderate') || description.includes('Marginal')) {
      return '👍';
    }
    if (description.includes('Failure')) {
      return '❌';
    }
    return '🎲';
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

  if (rollHistory.length === 0) {
    return (
      <div className="text-center py-8">
        <ClockIcon className="mx-auto h-8 w-8 text-gray-500" />
        <p className="mt-2 text-sm text-gray-500">
          No roll history yet
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      {rollHistory.slice(0, 10).map((roll) => (
        <div
          key={roll.rollId}
          className="p-3 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors duration-200"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1 min-w-0">
              <div className="flex items-center">
                <span className="text-lg mr-2">{getResultEmoji(roll.description)}</span>
                <span className={`text-sm font-medium truncate ${getResultColor(roll.description)}`}>
                  {roll.description}
                </span>
              </div>
              <div className="flex items-center mt-1 text-xs text-gray-400">
                <span>{roll.pool}d10 • {roll.descriptionLevel}</span>
                {roll.charactername && (
                  <span className="ml-2">• {roll.charactername}</span>
                )}
              </div>
              {roll.notes && (
                <p className="text-xs text-gray-500 mt-1 truncate italic">
                  "{roll.notes}"
                </p>
              )}
            </div>
            <div className="text-right ml-2">
              <div className="text-xs font-bold text-white">
                {roll.successes}/{roll.complications}
              </div>
              <div className="text-xs text-gray-500">
                {new Date(roll.rolledat || new Date()).toLocaleTimeString([], { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default RollHistory;

