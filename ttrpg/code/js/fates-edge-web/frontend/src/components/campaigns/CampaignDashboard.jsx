import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCampaignStore } from '../../store/campaignStore';
import { useAuthStore } from '../../store/authStore';
import CampaignHeader from './dashboard/CampaignHeader';
import PlayerList from './dashboard/PlayerList';
import SessionList from './dashboard/SessionList';
import CampaignClocks from './dashboard/CampaignClocks';
import ChatInterface from '../chat/ChatInterface';

const CampaignDashboard = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { getCampaign, currentCampaign, isLoading, error, clearError } = useCampaignStore();
  const { user } = useAuthStore();

  useEffect(() => {
    const fetchCampaign = async () => {
      try {
        await getCampaign(id);
      } catch (err) {
        console.error('Failed to fetch campaign:', err);
      }
    };

    if (id) {
      fetchCampaign();
    }
  }, [id, getCampaign]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <svg className="animate-spin h-12 w-12 text-purple-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-900 p-4">
        <div className="flex justify-between">
          <div className="text-sm text-red-200">
            {error}
          </div>
          <button
            onClick={() => {
              clearError();
              navigate('/dashboard');
            }}
            className="text-sm text-red-200 hover:text-white"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  if (!currentCampaign) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-gray-200">Campaign not found</h3>
        <button
          onClick={() => navigate('/dashboard')}
          className="mt-4 btn-primary"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  const isGM = currentCampaign.gmid === user?.userid;
  const isPlayer = currentCampaign.players?.includes(user?.userid);

  if (!isGM && !isPlayer) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-gray-200">Access denied</h3>
        <p className="mt-1 text-sm text-gray-400">
          You don't have permission to view this campaign.
        </p>
        <button
          onClick={() => navigate('/dashboard')}
          className="mt-4 btn-primary"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <CampaignHeader campaign={currentCampaign} isGM={isGM} />
      
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <CampaignClocks campaign={currentCampaign} isGM={isGM} />
          <SessionList campaign={currentCampaign} isGM={isGM} />
        </div>
        <div className="space-y-6">
          <PlayerList campaign={currentCampaign} isGM={isGM} />
        </div>
      </div>
    </div>
  );
};

export default CampaignDashboard;

