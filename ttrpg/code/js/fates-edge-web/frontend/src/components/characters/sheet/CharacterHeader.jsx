import React from 'react';
import { ArrowLeftIcon, PencilIcon } from '@heroicons/react/24/outline';

const CharacterHeader = ({ character }) => {
  const xpAvailable = character.xptotal - character.xpspent;
  const xpPercentage = character.xptotal > 0 ? (xpAvailable / character.xptotal) * 100 : 0;

  return (
    <div className="bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <button className="mr-4 text-gray-400 hover:text-white">
            <ArrowLeftIcon className="h-5 w-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-white">{character.name}</h1>
            <p className="text-gray-400">{character.archetype}</p>
          </div>
        </div>
        <button className="btn-secondary flex items-center">
          <PencilIcon className="h-4 w-4 mr-1" />
          Edit
        </button>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-4">
        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="h-8 w-8 rounded-full bg-purple-500 flex items-center justify-center">
                <span className="text-white text-sm font-bold">XP</span>
              </div>
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-300">Available XP</h3>
              <p className="text-2xl font-bold text-white">{xpAvailable}</p>
            </div>
          </div>
          <div className="mt-3 w-full bg-gray-600 rounded-full h-2">
            <div 
              className="bg-purple-600 h-2 rounded-full" 
              style={{ width: `${xpPercentage}%` }}
            ></div>
          </div>
          <p className="mt-1 text-xs text-gray-400">
            {character.xpspent} spent of {character.xptotal} total
          </p>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-300">Boons</h3>
          <p className="text-2xl font-bold text-white">{character.boons || 0}</p>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-300">Skills</h3>
          <p className="text-2xl font-bold text-white">{character.skills?.length || 0}</p>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-300">Last Updated</h3>
          <p className="text-sm text-white">
            {new Date(character.lastupdated).toLocaleDateString()}
          </p>
        </div>
      </div>
    </div>
  );
};

export default CharacterHeader;

