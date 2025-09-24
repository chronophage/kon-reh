import React, { useState } from 'react';
import { useCharacterStore } from '../../../../store/characterStore';
import { PlusIcon, MinusIcon } from '@heroicons/react/24/outline';

const AttributesTab = ({ character }) => {
  const { updateCharacter, advanceCharacter } = useCharacterStore();
  const [attributes, setAttributes] = useState(character.attributes || {
    body: 0,
    wits: 0,
    spirit: 0,
    presence: 0
  });
  const [isSaving, setIsSaving] = useState(false);

  const attributeDescriptions = {
    body: 'Physical prowess, endurance, and combat ability',
    wits: 'Mental acuity, knowledge, and analytical skills',
    spirit: 'Willpower, intuition, and connection to the supernatural',
    presence: 'Charisma, leadership, and social influence'
  };

  const handleAttributeChange = async (attr, value) => {
    const newAttributes = { ...attributes, [attr]: Math.max(0, value) };
    setAttributes(newAttributes);
    
    try {
      setIsSaving(true);
      await updateCharacter(character.characterid, { attributes: newAttributes });
    } catch (error) {
      console.error('Failed to update attributes:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleSpendXp = async (attr) => {
    const xpCost = attributes[attr] + 1; // Cost equals current rating + 1
    const xpAvailable = character.xptotal - character.xpspent;
    
    if (xpAvailable >= xpCost) {
      try {
        setIsSaving(true);
        await advanceCharacter(character.characterid, xpCost);
        await handleAttributeChange(attr, attributes[attr] + 1);
      } catch (error) {
        console.error('Failed to spend XP:', error);
      } finally {
        setIsSaving(false);
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Attributes</h2>
        <div className="text-sm text-gray-400">
          XP Available: {character.xptotal - character.xpspent}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {Object.entries(attributes).map(([attr, value]) => (
          <div key={attr} className="bg-gray-700 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-white capitalize">{attr}</h3>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handleAttributeChange(attr, value - 1)}
                  disabled={isSaving || value <= 0}
                  className="p-1 rounded-full bg-gray-600 text-gray-300 hover:bg-gray-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <MinusIcon className="h-4 w-4" />
                </button>
                <span className="text-2xl font-bold text-white w-8 text-center">{value}</span>
                <button
                  onClick={() => handleAttributeChange(attr, value + 1)}
                  disabled={isSaving}
                  className="p-1 rounded-full bg-gray-600 text-gray-300 hover:bg-gray-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <PlusIcon className="h-4 w-4" />
                </button>
              </div>
            </div>
            <p className="mt-3 text-sm text-gray-300">{attributeDescriptions[attr]}</p>
            <div className="mt-4">
              <button
                onClick={() => handleSpendXp(attr)}
                disabled={isSaving || (character.xptotal - character.xpspent) < (value + 1)}
                className="w-full btn-secondary text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSaving ? 'Saving...' : `Spend ${value + 1} XP`}
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-gray-700 rounded-lg p-6">
        <h3 className="text-lg font-medium text-white mb-4">Attribute Ratings Guide</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <h4 className="font-medium text-gray-300">Dice Pool Modifiers</h4>
            <ul className="mt-2 space-y-1 text-sm text-gray-400">
              <li>• 0: -2 dice to pool</li>
              <li>• 1-2: No modifier</li>
              <li>• 3-4: +1 dice to pool</li>
              <li>• 5-6: +2 dice to pool</li>
              <li>• 7+: +3 dice to pool</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-300">Stress Thresholds</h4>
            <ul className="mt-2 space-y-1 text-sm text-gray-400">
              <li>• Body: Physical stress</li>
              <li>• Wits: Mental stress</li>
              <li>• Spirit: Spiritual stress</li>
              <li>• Presence: Social stress</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AttributesTab;

