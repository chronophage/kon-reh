import React, { useState } from 'react';
import { useDiceStore } from '../../store/diceStore';
import { useCharacterStore } from '../../store/characterStore';
import DiceDisplay from './DiceDisplay';
import RollControls from './RollControls';
import RollHistory from './RollHistory';
import ComplicationDrawer from './ComplicationDrawer';

const DiceRoller = () => {
  const { currentRoll, isRolling, rollDice, error, clearError } = useDiceStore();
  const { characters } = useCharacterStore();
  const [showComplications, setShowComplications] = useState(false);

  const handleRoll = async (rollConfig) => {
    try {
      await rollDice(rollConfig);
    } catch (err) {
      console.error('Roll failed:', err);
    }
  };

  const handleDrawComplications = async (points) => {
    setShowComplications(true);
    // In a real implementation, this would call the store method
    // For now, we'll just show the drawer
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Dice Roller</h1>
        <p className="mt-1 text-gray-400">
          Roll Fate's Edge dice pools with description levels
        </p>
      </div>

      {error && (
        <div className="rounded-md bg-red-900 p-4">
          <div className="flex justify-between">
            <div className="text-sm text-red-200">
              {error}
            </div>
            <button
              onClick={clearError}
              className="text-sm text-red-200 hover:text-white"
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          {/* Dice Display */}
          <div className="bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-lg font-medium text-white mb-4">Current Roll</h2>
            <DiceDisplay 
              roll={currentRoll} 
              isRolling={isRolling} 
            />
          </div>

          {/* Roll Controls */}
          <div className="bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-lg font-medium text-white mb-4">Roll Configuration</h2>
            <RollControls 
              characters={characters}
              onRoll={handleRoll}
              onDrawComplications={handleDrawComplications}
              isRolling={isRolling}
            />
          </div>
        </div>

        <div className="space-y-6">
          {/* Roll History */}
          <div className="bg-gray-800 rounded-lg shadow">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-700">
              <h2 className="text-lg font-medium text-white">Recent Rolls</h2>
            </div>
            <div className="p-6">
              <RollHistory />
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-lg font-medium text-white mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <button
                onClick={() => handleDrawComplications(1)}
                className="w-full btn-secondary text-left"
              >
                Draw 1 Complication
              </button>
              <button
                onClick={() => handleDrawComplications(2)}
                className="w-full btn-secondary text-left"
              >
                Draw 2 Complications
              </button>
              <button
                onClick={() => handleDrawComplications(3)}
                className="w-full btn-secondary text-left"
              >
                Draw 3 Complications
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Complication Drawer */}
      {showComplications && (
        <ComplicationDrawer 
          onClose={() => setShowComplications(false)}
          onDraw={handleDrawComplications}
        />
      )}
    </div>
  );
};

export default DiceRoller;

