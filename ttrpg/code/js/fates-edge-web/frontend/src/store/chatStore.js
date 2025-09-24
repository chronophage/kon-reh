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

  // Join campaign chat
  joinCampaign: async (campaignId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/chat/messages/${campaignId}`);
      set({ 
        messages: response.data,
        isLoading: false 
      });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to join campaign chat';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Send message
  sendMessage: async (messageData) => {
    set({ error: null });
    try {
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

  // Get channel messages
  getChannelMessages: async (campaignId, channel) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get(`/chat/messages/${campaignId}/${channel}`);
      set({ 
        messages: response.data,
        currentChannel: channel,
        isLoading: false 
      });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch messages';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  // Add message to store
  addMessage: (message) => {
    set(state => ({
      messages: [...state.messages, message]
    }));
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

