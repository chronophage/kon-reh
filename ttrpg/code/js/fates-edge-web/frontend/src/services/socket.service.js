// frontend/src/services/socket.service.js
import { io } from 'socket.io-client';
import { useAuthStore } from '../store/authStore';

class SocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  connect() {
    const { token, user } = useAuthStore.getState();
    
    if (!token || !user) {
      console.error('Cannot connect to socket: No authentication token or user');
      return;
    }

    // Disconnect existing connection if any
    if (this.socket) {
      this.disconnect();
    }

    // Create new socket connection
    this.socket = io(process.env.REACT_APP_SOCKET_URL || 'http://localhost:3001', {
      auth: {
        token: token,
        userId: user.userid
      },
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: this.maxReconnectAttempts,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000
    });

    this.setupEventListeners();
  }

  setupEventListeners() {
    this.socket.on('connect', () => {
      console.log('Socket connected');
      this.isConnected = true;
      this.reconnectAttempts = 0;
    });

    this.socket.on('disconnect', (reason) => {
      console.log('Socket disconnected:', reason);
      this.isConnected = false;
    });

    this.socket.on('connect_error', (error) => {
      console.error('Socket connection error:', error);
      this.isConnected = false;
    });

    this.socket.on('error', (error) => {
      console.error('Socket error:', error);
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
    }
  }

  // Campaign room management
  joinCampaign(campaignId) {
    if (!this.socket) {
      console.error('Socket not connected');
      return;
    }
    this.socket.emit('join_campaign', campaignId);
  }

  leaveCampaign(campaignId) {
    if (!this.socket) {
      console.error('Socket not connected');
      return;
    }
    this.socket.emit('leave_campaign', campaignId);
  }

  // Chat functionality
  sendMessage(messageData) {
    if (!this.socket) {
      console.error('Socket not connected');
      return;
    }
    this.socket.emit('send_message', messageData);
  }

  onNewMessage(callback) {
    if (!this.socket) {
      console.error('Socket not connected');
      return;
    }
    this.socket.on('new_message', callback);
  }

  // Typing indicators
  sendTyping(campaignId, isTyping) {
    if (!this.socket) {
      console.error('Socket not connected');
      return;
    }
    this.socket.emit('typing', { campaignId, isTyping });
  }

  onUserTyping(callback) {
    if (!this.socket) {
      console.error('Socket not connected');
      return;
    }
    this.socket.on('user_typing', callback);
  }

  // Remove all listeners
  removeAllListeners() {
    if (this.socket) {
      this.socket.removeAllListeners();
    }
  }
}

// Export singleton instance
export default new SocketService();

