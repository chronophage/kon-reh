// frontend/src/components/campaigns/CampaignList.jsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCampaignStore } from '../../store/campaignStore';
import { useAuthStore } from '../../store/authStore';

const CampaignList = () => {
  const navigate = useNavigate();
  const { campaigns, getUserCampaigns, isLoading, error } = useCampaignStore();
  const { user } = useAuthStore();

  useEffect(() => {
    if (user?.userid) {
      getUserCampaigns();
    }
  }, [user, getUserCampaigns]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-fate-accent">Loading campaigns...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-900/50 border border-red-700 rounded-lg p-4">
          <h3 className="text-red-300 font-medium">Error loading campaigns</h3>
          <p className="text-red-200 mt-1">{error}</p>
          <button
            onClick={() => getUserCampaigns()}
            className="mt-3 btn-primary"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-fate-accent">My Campaigns</h1>
        <button
          onClick={() => navigate('/campaigns/create')}
          className="btn-primary"
        >
          Create Campaign
        </button>
      </div>

      {campaigns.length === 0 ? (
        <div className="bg-fate-dark rounded-lg p-8 text-center">
          <div className="text-fate-accent text-xl mb-2">No campaigns yet</div>
          <p className="text-gray-400 mb-4">Create your first campaign to get started</p>
          <button
            onClick={() => navigate('/campaigns/create')}
            className="btn-primary"
          >
            Create Campaign
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {campaigns.map((campaign) => (
            <div 
              key={campaign.campaignid} 
              className="bg-fate-dark rounded-lg p-6 hover:bg-fate-darker transition-colors cursor-pointer border border-fate-dark hover:border-fate-accent"
              onClick={() => navigate(`/campaigns/${campaign.campaignid}`)}
            >
              <h3 className="text-xl font-bold text-fate-accent mb-2">{campaign.name}</h3>
              <p className="text-gray-300 mb-4 line-clamp-2">{campaign.description}</p>
              <div className="flex justify-between items-center text-sm text-gray-400">
                <span>Players: {campaign.players?.length || 0}</span>
                <span>{campaign.gmuserid === user?.userid ? 'GM' : 'Player'}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CampaignList;

