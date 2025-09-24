import { create } from 'zustand';
import api from '../services/api';

const useCharacterStore = create((set, get) => ({
  characters: [],
  currentCharacter: null,
  isLoading: false,
  error: null,

  // Get all characters for user
  getUserCharacters: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/characters/${get().userId}`);
      set({ characters: response.data, isLoading: false });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch characters';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Create new character
  createCharacter: async (characterData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post('/characters', characterData);
      const newCharacter = response.data;
      set(state => ({
        characters: [...state.characters, newCharacter],
        isLoading: false
      }));
      return newCharacter;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to create character';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Get character by ID
  getCharacter: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/characters/${id}`);
      set({ currentCharacter: response.data, isLoading: false });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch character';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Update character
  updateCharacter: async (id, updateData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.put(`/characters/${id}`, updateData);
      const updatedCharacter = response.data;
      
      set(state => ({
        characters: state.characters.map(char => 
          char.characterid === id ? updatedCharacter : char
        ),
        currentCharacter: updatedCharacter,
        isLoading: false
      }));
      
      return updatedCharacter;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to update character';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Delete character
  deleteCharacter: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await api.delete(`/characters/${id}`);
      set(state => ({
        characters: state.characters.filter(char => char.characterid !== id),
        currentCharacter: state.currentCharacter?.characterid === id ? null : state.currentCharacter,
        isLoading: false
      }));
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to delete character';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Advance character (spend XP)
  advanceCharacter: async (id, xpSpent) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post(`/characters/${id}/advance`, { xpSpent });
      const updatedCharacter = response.data.character;
      
      set(state => ({
        characters: state.characters.map(char => 
          char.characterid === id ? updatedCharacter : char
        ),
        currentCharacter: updatedCharacter,
        isLoading: false
      }));
      
      return updatedCharacter;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to advance character';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Set current character
  setCurrentCharacter: (character) => {
    set({ currentCharacter: character });
  },

  // Clear error
  clearError: () => set({ error: null })
}));

export { useCharacterStore };

