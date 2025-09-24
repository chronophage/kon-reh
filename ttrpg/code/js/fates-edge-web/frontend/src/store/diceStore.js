import { create } from 'zustand';
import api from '../services/api';

const useDiceStore = create((set, get) => ({
  rollHistory: [],
  currentRoll: null,
  isRolling: false,
  error: null,

  // Roll dice
  rollDice: async (rollData) => {
    set({ isRolling: true, error: null });
    try {
      const response = await api.post('/roll', rollData);
      const rollResult = response.data;
      
      set(state => ({
        currentRoll: rollResult,
        rollHistory: [rollResult, ...state.rollHistory.slice(0, 49)], // Keep last 50 rolls
        isRolling: false
      }));
      
      return rollResult;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to roll dice';
      set({ error: errorMessage, isRolling: false });
      throw error;
    }
  },

  // Get roll history for character
  getRollHistory: async (characterId) => {
    set({ error: null });
    try {
      const response = await api.get(`/roll/history/${characterId}`);
      set({ rollHistory: response.data });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch roll history';
      set({ error: errorMessage });
      throw error;
    }
  },

  // Draw complications
  drawComplications: async (points, gmSpends = []) => {
    set({ error: null });
    try {
      const response = await api.post('/roll/complications', { points, gmSpends });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to draw complications';
      set({ error: errorMessage });
      throw error;
    }
  },

  // Clear current roll
  clearCurrentRoll: () => set({ currentRoll: null }),

  // Clear error
  clearError: () => set({ error: null })
}));

export { useDiceStore };

