import React from 'react';
import { UserGroupIcon, CalendarIcon, PencilIcon } from '@heroicons/react/24/outline';

const CampaignHeader = ({ campaign, isGM }) => {
  const playerCount = (campaign.players?.length || 0) + 1; // +1 for GM
  const statusColor = campaign.status === 'active' ? 'bg-green-900 text-green-200' : 'bg-gray-900 text-gray-200';

  return (
    <div className="bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">{campaign.name}</h1>
          <p className="text-gray-400 mt-1">{campaign.description || 'No description provided'}</p>
        </div>
        {isGM && (
          <button className="btn-secondary flex items-center">
            <PencilIcon className="h-4 w-4 mr-1" />
            Edit
          </button>
        )}
      </div>

      <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <UserGroupIcon className="h-6 w-6 text-purple-400" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-300">Players</h3>
              <p className="text-2xl font-bold text-white">{playerCount}</p>
            </div>
          </div>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CalendarIcon className="h-6 w-6 text-blue-400" />
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-300">Status</h3>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColor}`}>
                {campaign.status}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div className="ml-4">
              <h3 className="text-sm font-medium text-gray-300">Created</h3>
              <p className="text-sm text-white">
                {new Date(campaign.createdat).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CampaignHeader;

