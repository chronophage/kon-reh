import { create } from 'zustand';
import api from '../services/api';

const useMacroStore = create((set, get) => ({
  macros: [],
  pendingMacros: [],
  isLoading: false,
  error: null,

  // Get campaign macros
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

  // Get user macros
  getUserMacros: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get('/macros/user');
      set({ macros: response.data, isLoading: false });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch user macros';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Get pending macros (GM only)
  getPendingMacros: async (campaignId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/macros/pending/${campaignId}`);
      set({ pendingMacros: response.data, isLoading: false });
      return response.data;
    } catch (error) {
      // Not an error if user is not GM
      if (error.response?.status !== 403) {
        const errorMessage = error.response?.data?.message || 'Failed to fetch pending macros';
        set({ error: errorMessage, isLoading: false });
      }
      set({ isLoading: false });
      return [];
    }
  },

  // Create macro
  createMacro: async (macroData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post('/macros', macroData);
      const newMacro = response.data.macro;
      
      set(state => ({
        macros: [...state.macros, newMacro],
        isLoading: false
      }));
      
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to create macro';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Update macro
  updateMacro: async (macroId, updateData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.put(`/macros/${macroId}`, updateData);
      const updatedMacro = response.data.macro;
      
      set(state => ({
        macros: state.macros.map(macro => 
          macro.macroid === macroId ? updatedMacro : macro
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
  deleteMacro: async (macroId) => {
    set({ isLoading: true, error: null });
    try {
      await api.delete(`/macros/${macroId}`);
      
      set(state => ({
        macros: state.macros.filter(macro => macro.macroid !== macroId),
        isLoading: false
      }));
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to delete macro';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Approve macro (GM only)
  approveMacro: async (macroId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.patch(`/macros/${macroId}/approve`);
      const approvedMacro = response.data.macro;
      
      set(state => ({
        macros: state.macros.map(macro => 
          macro.macroid === macroId ? approvedMacro : macro
        ),
        pendingMacros: state.pendingMacros.filter(macro => macro.macroid !== macroId),
        isLoading: false
      }));
      
      return approvedMacro;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to approve macro';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Clear error
  clearError: () => set({ error: null })
}));

export { useMacroStore };

