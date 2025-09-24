const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const dotenv = require('dotenv');
const http = require('http');
const { Server } = require('socket.io');

dotenv.config();

const app = express();
const server = http.createServer(app);
const PORT = process.env.PORT || 3001;

// Store active users and sockets
const activeUsers = new Map();

// Initialize Socket.IO
const io = new Server(server, {
  cors: {
    origin: process.env.FRONTEND_URL || "http://localhost:3000",
    methods: ["GET", "POST"],
    credentials: true
  }
});

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Store io instance for use in routes
app.set('io', io);

// Routes
app.get('/', (req, res) => {
  res.json({ message: 'Fate\'s Edge API Server' });
});

// Auth routes
app.use('/api/auth', require('./routes/auth.routes'));

// Character routes
app.use('/api/characters', require('./routes/characters.routes'));

// Campaign routes
app.use('/api/campaigns', require('./routes/campaigns.routes'));

// Roll routes
app.use('/api/roll', require('./routes/roll.routes'));

// Chat routes
app.use('/api/chat', require('./routes/chat.routes'));

// Macro routes
app.use('/api/macros', require('./routes/macros.routes'));

// Socket.IO connection handling
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) {
    return next(new Error('Authentication error'));
  }
  
  // Here you would verify the JWT token
  // For now, we'll store the user ID directly
  // In production, verify the token and extract user ID
  socket.userId = socket.handshake.auth.userId;
  next();
});

io.on('connection', (socket) => {
  console.log('User connected:', socket.userId);
  
  // Store user connection
  if (socket.userId) {
    if (!activeUsers.has(socket.userId)) {
      activeUsers.set(socket.userId, new Set());
    }
    activeUsers.get(socket.userId).add(socket.id);
  }

  // Join campaign rooms
  socket.on('join_campaign', (campaignId) => {
    socket.join(`campaign_${campaignId}`);
    console.log(`User ${socket.userId} joined campaign ${campaignId}`);
    
    // Notify others in campaign that user joined
    socket.to(`campaign_${campaignId}`).emit('user_joined', {
      userId: socket.userId,
      timestamp: new Date()
    });
  });

  // Leave campaign room
  socket.on('leave_campaign', (campaignId) => {
    socket.leave(`campaign_${campaignId}`);
    console.log(`User ${socket.userId} left campaign ${campaignId}`);
  });

  // Send chat message
  socket.on('send_message', async (data) => {
    try {
      const { campaignId, content, channel = 'general', targetUserId = null, characterId = null } = data;
      
      // Verify user is in campaign (you'd want to add proper auth here)
      // For now, we'll assume the user is authorized
      
      // Emit message to campaign room
      const messageData = {
        campaignId,
        userId: socket.userId,
        characterId,
        content,
        channel,
        targetUserId,
        timestamp: new Date(),
        username: 'User_' + socket.userId.substring(0, 8), // Placeholder - get real username
        charactername: characterId ? 'Character' : null // Placeholder - get real character name
      };
      
      // Emit to campaign room
      io.to(`campaign_${campaignId}`).emit('new_message', messageData);
      
    } catch (error) {
      console.error('Socket message error:', error);
      socket.emit('error', { message: 'Error sending message' });
    }
  });

  // Roll dice
  socket.on('roll_dice', async (data) => {
    try {
      const { campaignId, pool, descriptionLevel = 'Basic', characterId, notes } = data;
      
      // Perform dice roll (same logic as API)
      const dice = Array.from({ length: pool }, () => Math.floor(Math.random() * 10) + 1);
      let successes = dice.filter(d => d >= 6).length;
      let complications = dice.filter(d => d === 1).length;
      
      // Apply description ladder benefits
      if (descriptionLevel === 'Detailed' && complications > 0) {
        const oneIndex = dice.indexOf(1);
        if (oneIndex !== -1) {
          const newRoll = Math.floor(Math.random() * 10) + 1;
          dice[oneIndex] = newRoll;
          if (newRoll >= 6) successes++;
          if (newRoll === 1) complications++;
          else complications--;
        }
      } else if (descriptionLevel === 'Intricate' && complications > 0) {
        for (let i = 0; i < dice.length; i++) {
          if (dice[i] === 1) {
            const newRoll = Math.floor(Math.random() * 10) + 1;
            dice[i] = newRoll;
            if (newRoll >= 6) successes++;
            if (newRoll === 1) complications++;
            else complications--;
          }
        }
      }
      
      const rollResult = {
        dice,
        successes,
        complications,
        pool,
        descriptionLevel,
        characterId,
        notes,
        userId: socket.userId,
        timestamp: new Date()
      };
      
      // Emit roll result to campaign
      io.to(`campaign_${campaignId}`).emit('dice_rolled', rollResult);
      
    } catch (error) {
      console.error('Socket roll error:', error);
      socket.emit('error', { message: 'Error rolling dice' });
    }
  });

  // Macro execution
  socket.on('execute_macro', async (data) => {
    try {
      const { campaignId, macroId, macroName, macroCommand } = data;
      
      const macroResult = {
        macroId,
        macroName,
        macroCommand,
        userId: socket.userId,
        timestamp: new Date()
      };
      
      // Emit macro execution to campaign
      io.to(`campaign_${campaignId}`).emit('macro_executed', macroResult);
      
    } catch (error) {
      console.error('Socket macro error:', error);
      socket.emit('error', { message: 'Error executing macro' });
    }
  });

  // GM actions
  socket.on('gm_action', async (data) => {
    try {
      const { campaignId, action, payload } = data;
      
      // Emit GM action to campaign
      io.to(`campaign_${campaignId}`).emit('gm_action_broadcast', {
        action,
        payload,
        userId: socket.userId,
        timestamp: new Date()
      });
      
    } catch (error) {
      console.error('Socket GM action error:', error);
      socket.emit('error', { message: 'Error executing GM action' });
    }
  });

  // User typing indicator
  socket.on('typing', (data) => {
    const { campaignId, isTyping } = data;
    socket.to(`campaign_${campaignId}`).emit('user_typing', {
      userId: socket.userId,
      isTyping,
      timestamp: new Date()
    });
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.userId);
    
    // Remove user from active users
    if (socket.userId && activeUsers.has(socket.userId)) {
      const userSockets = activeUsers.get(socket.userId);
      userSockets.delete(socket.id);
      
      if (userSockets.size === 0) {
        activeUsers.delete(socket.userId);
      }
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ message: 'Something went wrong!' });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Process terminated');
  });
});

