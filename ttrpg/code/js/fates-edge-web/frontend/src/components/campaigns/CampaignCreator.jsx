// frontend/src/components/campaigns/CampaignCreator.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCampaignStore } from '../../store/campaignStore';

const CampaignCreator = () => {
  const navigate = useNavigate();
  const { createCampaign, isLoading, error } = useCampaignStore();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    setting: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newCampaign = await createCampaign(formData);
      navigate(`/campaigns/${newCampaign.campaignid}`);
    } catch (err) {
      console.error('Failed to create campaign:', err);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="bg-fate-dark rounded-lg p-6">
        <h1 className="text-2xl font-bold text-fate-accent mb-6">Create New Campaign</h1>
        
        {error && (
          <div className="bg-red-900/50 border border-red-700 rounded-lg p-4 mb-6">
            <p className="text-red-200">{error}</p>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Campaign Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="input-field w-full"
              placeholder="Enter campaign name"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              className="input-field w-full"
              placeholder="Describe your campaign"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Setting
            </label>
            <input
              type="text"
              name="setting"
              value={formData.setting}
              onChange={handleChange}
              className="input-field w-full"
              placeholder="Campaign setting (e.g., Cyberpunk, Fantasy, etc.)"
            />
          </div>
          
          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={() => navigate('/campaigns')}
              className="px-4 py-2 border border-gray-600 rounded-lg text-gray-300 hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary flex items-center"
            >
              {isLoading && (
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              )}
              {isLoading ? 'Creating...' : 'Create Campaign'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CampaignCreator;

