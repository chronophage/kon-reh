import React, { useState } from 'react';
import { UserIcon, UserPlusIcon, UserMinusIcon } from '@heroicons/react/24/outline';
import { useCampaignStore } from '../../../store/campaignStore';
import { useAuthStore } from '../../../store/authStore';

const PlayerList = ({ campaign, isGM }) => {
  const { invitePlayer, removePlayer } = useCampaignStore();
  const { user } = useAuthStore();
  const [newPlayerEmail, setNewPlayerEmail] = useState('');
  const [isInviting, setIsInviting] = useState(false);

  const handleInvitePlayer = async (e) => {
    e.preventDefault();
    if (!newPlayerEmail.trim()) return;
    
    // In a real app, you'd look up the user by email first
    // For now, we'll just show the form
    alert('In a real implementation, this would invite a player by email');
    setNewPlayerEmail('');
  };

  const handleRemovePlayer = async (userId) => {
    if (window.confirm('Are you sure you want to remove this player from the campaign?')) {
      try {
        await removePlayer(campaign.campaignid, userId);
      } catch (error) {
        console.error('Failed to remove player:', error);
      }
    }
  };

  const players = campaign.players || [];
  const allPlayers = [campaign.gmid, ...players];

  return (
    <div className="bg-gray-800 rounded-lg shadow">
      <div className="px-4 py-5 sm:px-6 border-b border-gray-700">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-medium text-white">Players</h2>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-900 text-purple-200">
            {allPlayers.length}
          </span>
        </div>
      </div>
      <div className="p-6">
        <div className="space-y-4">
          {/* GM */}
          <div className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
            <div className="flex items-center">
              <div className="flex-shrink-0 h-10 w-10 rounded-full bg-purple-600 flex items-center justify-center">
                <UserIcon className="h-6 w-6 text-white" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-white">Game Master</p>
                <p className="text-xs text-gray-400">You</p>
              </div>
            </div>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-800 text-yellow-200">
              GM
            </span>
          </div>

          {/* Players */}
          {players.map((playerId, index) => (
            <div key={playerId} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
              <div className="flex items-center">
                <div className="flex-shrink-0 h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center">
                  <UserIcon className="h-6 w-6 text-white" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-white">Player {index + 1}</p>
                  <p className="text-xs text-gray-400">player{index + 1}@example.com</p>
                </div>
              </div>
              {isGM && (
                <button
                  onClick={() => handleRemovePlayer(playerId)}
                  className="p-1 rounded-full bg-red-900 text-red-300 hover:bg-red-800"
                >
                  <UserMinusIcon className="h-4 w-4" />
                </button>
              )}
            </div>
          ))}

          {/* Invite Player Form (GM only) */}
          {isGM && (
            <form onSubmit={handleInvitePlayer} className="mt-4 pt-4 border-t border-gray-700">
              <h3 className="text-sm font-medium text-gray-300 mb-2">Invite Player</h3>
              <div className="flex space-x-2">
                <input
                  type="email"
                  value={newPlayerEmail}
                  onChange={(e) => setNewPlayerEmail(e.target.value)}
                  className="input-field flex-1 text-sm"
                  placeholder="player@example.com"
                />
                <button
                  type="submit"
                  disabled={isInviting || !newPlayerEmail.trim()}
                  className="btn-primary flex items-center text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <UserPlusIcon className="h-4 w-4 mr-1" />
                  Invite
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default PlayerList;

