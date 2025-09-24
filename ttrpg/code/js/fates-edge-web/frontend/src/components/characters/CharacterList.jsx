import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCharacterStore } from '../../store/characterStore';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';

const CharacterList = () => {
  const navigate = useNavigate();
  const { characters, getUserCharacters, deleteCharacter, isLoading, error } = useCharacterStore();

  useEffect(() => {
    getUserCharacters();
  }, [getUserCharacters]);

  const handleCreateCharacter = () => {
    navigate('/characters/new');
  };

  const handleEditCharacter = (id) => {
    navigate(`/characters/${id}`);
  };

  const handleDeleteCharacter = async (id, name) => {
    if (window.confirm(`Are you sure you want to delete ${name}? This action cannot be undone.`)) {
      try {
        await deleteCharacter(id);
      } catch (error) {
        console.error('Failed to delete character:', error);
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">My Characters</h1>
          <p className="mt-1 text-gray-400">Manage your Fate's Edge characters</p>
        </div>
        <button
          onClick={handleCreateCharacter}
          className="btn-primary flex items-center"
        >
          <PlusIcon className="h-4 w-4 mr-1" />
          New Character
        </button>
      </div>

      {error && (
        <div className="rounded-md bg-red-900 p-4">
          <div className="text-sm text-red-200">
            {error}
          </div>
        </div>
      )}

      {isLoading ? (
        <div className="flex justify-center py-12">
          <svg className="animate-spin h-12 w-12 text-purple-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      ) : characters.length > 0 ? (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {characters.map((character) => (
            <div key={character.characterid} className="bg-gray-800 rounded-lg shadow overflow-hidden">
              <div className="p-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium text-white">{character.name}</h3>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-900 text-purple-200">
                    {character.archetype}
                  </span>
                </div>
                <div className="mt-4 flex items-center text-sm text-gray-300">
                  <span>XP: {character.xptotal - character.xpspent}/{character.xptotal}</span>
                </div>
                <div className="mt-4 grid grid-cols-4 gap-2">
                  <div className="text-center">
                    <p className="text-xs text-gray-400">Body</p>
                    <p className="text-sm font-medium text-white">{character.attributes?.body || 0}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-gray-400">Wits</p>
                    <p className="text-sm font-medium text-white">{character.attributes?.wits || 0}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-gray-400">Spirit</p>
                    <p className="text-sm font-medium text-white">{character.attributes?.spirit || 0}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-gray-400">Presence</p>
                    <p className="text-sm font-medium text-white">{character.attributes?.presence || 0}</p>
                  </div>
                </div>
                <div className="mt-4 flex space-x-2">
                  <button
                    onClick={() => handleEditCharacter(character.characterid)}
                    className="flex-1 btn-secondary flex items-center justify-center text-xs"
                  >
                    <PencilIcon className="h-3 w-3 mr-1" />
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeleteCharacter(character.characterid, character.name)}
                    className="flex-1 btn-danger flex items-center justify-center text-xs"
                  >
                    <TrashIcon className="h-3 w-3 mr-1" />
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-200">No characters</h3>
          <p className="mt-1 text-sm text-gray-400">
            Get started by creating a new character.
          </p>
          <div className="mt-6">
            <button
              onClick={handleCreateCharacter}
              className="btn-primary inline-flex items-center"
            >
              <PlusIcon className="h-4 w-4 mr-1" />
              New Character
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CharacterList;

