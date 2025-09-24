const jwt = require('jsonwebtoken');

class SocketService {
  constructor(io) {
    this.io = io;
    this.activeUsers = new Map();
  }

  // Verify JWT token and extract user ID
  verifyToken(token) {
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      return decoded.userId;
    } catch (error) {
      throw new Error('Invalid token');
    }
  }

  // Add user to active users map
  addUser(userId, socketId) {
    if (!this.activeUsers.has(userId)) {
      this.activeUsers.set(userId, new Set());
    }
    this.activeUsers.get(userId).add(socketId);
  }

  // Remove user from active users map
  removeUser(userId, socketId) {
    if (this.activeUsers.has(userId)) {
      const userSockets = this.activeUsers.get(userId);
      userSockets.delete(socketId);
      
      if (userSockets.size === 0) {
        this.activeUsers.delete(userId);
      }
    }
  }

  // Get all socket IDs for a user
  getUserSockets(userId) {
    return this.activeUsers.get(userId) || new Set();
  }

  // Emit to specific user
  emitToUser(userId, event, data) {
    const userSockets = this.getUserSockets(userId);
    userSockets.forEach(socketId => {
      this.io.to(socketId).emit(event, data);
    });
  }

  // Emit to campaign room
  emitToCampaign(campaignId, event, data) {
    this.io.to(`campaign_${campaignId}`).emit(event, data);
  }

  // Get online users count for campaign
  getCampaignOnlineUsers(campaignId) {
    // This would need to track which users are in which campaigns
    // For now, return total active users
    return this.activeUsers.size;
  }
}

module.exports = SocketService;

