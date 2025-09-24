// frontend/src/store/campaignStore.js (updated)
import { create } from 'zustand';
import api from '../services/api';
import { useAuthStore } from './authStore';

const useCampaignStore = create((set, get) => ({
  campaigns: [],
  currentCampaign: null,
  isLoading: false,
  error: null,

  // Get all campaigns for user
  getUserCampaigns: async () => {
    set({ isLoading: true, error: null });
    try {
      const { user } = useAuthStore.getState();
      if (!user) throw new Error('User not authenticated');
      
      const response = await api.get(`/campaigns/user/${user.userid}`);
      set({ campaigns: response.data, isLoading: false });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch campaigns';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Create new campaign
  createCampaign: async (campaignData) => {
    set({ isLoading: true, error: null });
    try {
      const { user } = useAuthStore.getState();
      if (!user) throw new Error('User not authenticated');
      
      const response = await api.post('/campaigns', { ...campaignData, gmuserid: user.userid });
      const newCampaign = response.data;
      set(state => ({
        campaigns: [...state.campaigns, newCampaign],
        isLoading: false
      }));
      return newCampaign;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to create campaign';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Get campaign by ID
  getCampaign: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/campaigns/${id}`);
      set({ currentCampaign: response.data, isLoading: false });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch campaign';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Update campaign
  updateCampaign: async (id, updateData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.put(`/campaigns/${id}`, updateData);
      const updatedCampaign = response.data;
      
      set(state => ({
        campaigns: state.campaigns.map(camp => 
          camp.campaignid === id ? updatedCampaign : camp
        ),
        currentCampaign: updatedCampaign.campaignid === state.currentCampaign?.campaignid 
          ? updatedCampaign : state.currentCampaign,
        isLoading: false
      }));
      
      return updatedCampaign;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to update campaign';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Invite player to campaign
  invitePlayer: async (campaignId, email) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post(`/campaigns/${campaignId}/invite`, { email });
      const updatedCampaign = response.data.campaign;
      
      set(state => ({
        campaigns: state.campaigns.map(camp => 
          camp.campaignid === campaignId ? updatedCampaign : camp
        ),
        currentCampaign: updatedCampaign.campaignid === state.currentCampaign?.campaignid 
          ? updatedCampaign : state.currentCampaign,
        isLoading: false
      }));
      
      return updatedCampaign;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to invite player';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Remove player from campaign
  removePlayer: async (campaignId, userId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post(`/campaigns/${campaignId}/remove`, { userId });
      const updatedCampaign = response.data.campaign;
      
      set(state => ({
        campaigns: state.campaigns.map(camp => 
          camp.campaignid === campaignId ? updatedCampaign : camp
        ),
        currentCampaign: updatedCampaign.campaignid === state.currentCampaign?.campaignid 
          ? updatedCampaign : state.currentCampaign,
        isLoading: false
      }));
      
      return updatedCampaign;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to remove player';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Create session for campaign
  createSession: async (campaignId, sessionData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post(`/campaigns/${campaignId}/sessions`, sessionData);
      const newSession = response.data;
      
      // Update campaign with new session
      set(state => {
        const updatedCampaign = state.currentCampaign 
          ? { 
              ...state.currentCampaign,
              sessions: [...(state.currentCampaign.sessions || []), newSession]
            } 
          : state.campaigns.find(c => c.campaignid === campaignId);
        
        return {
          currentCampaign: updatedCampaign,
          isLoading: false
        };
      });
      
      return newSession;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to create session';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Clear error
  clearError: () => set({ error: null })
}));

export { useCampaignStore };

