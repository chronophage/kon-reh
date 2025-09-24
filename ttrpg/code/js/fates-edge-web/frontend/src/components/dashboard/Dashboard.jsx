import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { useCharacterStore } from '../../store/characterStore';
import { PlusIcon, UserGroupIcon, DiceIcon } from '@heroicons/react/24/outline';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const { characters, getUserCharacters, isLoading } = useCharacterStore();
  const [recentCharacters, setRecentCharacters] = useState([]);

  useEffect(() => {
    const fetchCharacters = async () => {
      try {
        await getUserCharacters();
      } catch (error) {
        console.error('Failed to fetch characters:', error);
      }
    };

    if (user) {
      fetchCharacters();
    }
  }, [user, getUserCharacters]);

  useEffect(() => {
    // Get 3 most recently updated characters
    const sorted = [...characters].sort((a, b) => 
      new Date(b.lastupdated) - new Date(a.lastupdated)
    );
    setRecentCharacters(sorted.slice(0, 3));
  }, [characters]);

  const handleCreateCharacter = () => {
    navigate('/characters/new');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Welcome back, {user?.username}</h1>
        <p className="mt-1 text-gray-400">
          {user?.role === 'gm' 
            ? 'Manage your campaigns and guide your players' 
            : 'Manage your characters and join campaigns'}
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-gray-800 overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
                <UserGroupIcon className="h-6 w-6 text-white" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-300 truncate">Your Characters</dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-white">{characters.length}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                <DiceIcon className="h-6 w-6 text-white" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-300 truncate">Campaigns</dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-white">0</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-300 truncate">Total XP</dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-white">
                      {characters.reduce((total, char) => total + char.xptotal, 0)}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Characters */}
      <div className="bg-gray-800 shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-medium text-white">Recent Characters</h2>
            <button
              onClick={handleCreateCharacter}
              className="btn-primary flex items-center"
            >
              <PlusIcon className="h-4 w-4 mr-1" />
              New Character
            </button>
          </div>
        </div>
        <div className="px-4 py-5 sm:p-6">
          {isLoading ? (
            <div className="flex justify-center py-8">
              <svg className="animate-spin h-8 w-8 text-purple-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
          ) : recentCharacters.length > 0 ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {recentCharacters.map((character) => (
                <div
                  key={character.characterid}
                  className="bg-gray-700 rounded-lg p-4 hover:bg-gray-600 transition-colors duration-200 cursor-pointer"
                  onClick={() => navigate(`/characters/${character.characterid}`)}
                >
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-white">{character.name}</h3>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-900 text-purple-200">
                      {character.archetype}
                    </span>
                  </div>
                  <div className="mt-2 flex items-center text-sm text-gray-300">
                    <span>XP: {character.xptotal - character.xpspent}/{character.xptotal}</span>
                  </div>
                  <div className="mt-3 flex space-x-4">
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
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <UserGroupIcon className="mx-auto h-12 w-12 text-gray-400" />
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
      </div>
    </div>
  );
};

export default Dashboard;

