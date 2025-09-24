// frontend/src/store/chatStore.js (updated)
import { create } from 'zustand';
import api from '../services/api';

const useChatStore = create((set, get) => ({
  messages: [],
  currentChannel: 'general',
  channels: ['general', 'ooc', 'private'],
  isLoading: false,
  error: null,
  isConnected: false,
  typingUsers: new Map(),

  // Initialize chat for campaign
  initCampaignChat: (campaignId) => {
    // Reset messages for new campaign
    set({ 
      messages: [],
      currentChannel: 'general'
    });
  },

  // Add message to store (called by socket listener)
  addMessage: (message) => {
    set(state => ({
      messages: [...state.messages, message]
    }));
  },

  // Send message through API (fallback) - but now we use SocketIO
  sendMessage: async (messageData) => {
    set({ error: null });
    try {
      // In real-time mode, we send via SocketIO instead
      // This is kept for backward compatibility or fallback
      const response = await api.post('/chat/messages', messageData);
      const newMessage = response.data;
      
      set(state => ({
        messages: [...state.messages, newMessage]
      }));
      
      return newMessage;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to send message';
      set({ error: errorMessage });
      throw error;
    }
  },

  // Set typing status
  setTyping: (userId, isTyping) => {
    set(state => {
      const newTypingUsers = new Map(state.typingUsers);
      if (isTyping) {
        newTypingUsers.set(userId, Date.now());
      } else {
        newTypingUsers.delete(userId);
      }
      return { typingUsers: newTypingUsers };
    });
  },

  // Clear old typing statuses
  clearOldTyping: () => {
    set(state => {
      const now = Date.now();
      const newTypingUsers = new Map(state.typingUsers);
      for (const [userId, timestamp] of newTypingUsers.entries()) {
        if (now - timestamp > 5000) { // 5 seconds
          newTypingUsers.delete(userId);
        }
      }
      return { typingUsers: newTypingUsers };
    });
  },

  // Switch channel
  switchChannel: (channel) => {
    set({ currentChannel: channel });
  },

  // Clear error
  clearError: () => set({ error: null })
}));

export { useChatStore };

