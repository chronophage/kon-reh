// frontend/src/store/macroStore.js (updated)
import { create } from 'zustand';
import api from '../services/api';

const useMacroStore = create((set, get) => ({
  macros: [],
  isLoading: false,
  error: null,

  // Get all macros for campaign
  getCampaignMacros: async (campaignId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/macros/campaign/${campaignId}`);
      set({ macros: response.data, isLoading: false });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch macros';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Create new macro
  createMacro: async (campaignId, macroData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post('/macros', { 
        campaignId, 
        ...macroData 
      });
      const newMacro = response.data;
      
      set(state => ({
        macros: [...state.macros, newMacro],
        isLoading: false
      }));
      
      return newMacro;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to create macro';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Update macro
  updateMacro: async (id, updateData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.put(`/macros/${id}`, updateData);
      const updatedMacro = response.data;
      
      set(state => ({
        macros: state.macros.map(macro => 
          macro.macroid === id ? updatedMacro : macro
        ),
        isLoading: false
      }));
      
      return updatedMacro;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to update macro';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Delete macro
  deleteMacro: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await api.delete(`/macros/${id}`);
      
      set(state => ({
        macros: state.macros.filter(macro => macro.macroid !== id),
        isLoading: false
      }));
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to delete macro';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Execute macro
  executeMacro: async (campaignId, macroCommand, characterId = null) => {
    set({ error: null });
    try {
      const response = await api.post('/macros/execute', {
        campaignId,
        macroCommand,
        characterId
      });
      
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to execute macro';
      set({ error: errorMessage });
      throw error;
    }
  },

  // Clear error
  clearError: () => set({ error: null })
}));

export { useMacroStore };

