// backend/server.js (updated with full security)
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const http = require('http');
const { Server } = require('socket.io');
const helmet = require('helmet');
const xss = require('xss-clean');
const mongoSanitize = require('express-mongo-sanitize');
const hpp = require('hpp');

// Security middleware
const { 
  generalLimiter, 
  authLimiter, 
  diceRollLimiter, 
  securityHeaders, 
  sanitizeInput,
  preventSQLInjection,
  preventXSS,
  csrfProtection 
} = require('./middleware/security.middleware');

dotenv.config();

const app = express();
const server = http.createServer(app);
const PORT = process.env.PORT || 3001;

// Store active users and sockets
const activeUsers = new Map();

// Initialize Socket.IO with security
const io = new Server(server, {
  cors: {
    origin: process.env.FRONTEND_URL || "http://localhost:3000",
    methods: ["GET", "POST"],
    credentials: true
  },
  // Security options
  allowEIO3: true,
  transports: ['websocket', 'polling']
});

// Store io instance for use in routes
app.set('io', io);

// Security middleware (order matters)
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://apis.google.com"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      fontSrc: ["'self'", "data:"],
      connectSrc: ["'self'", "ws:", "wss:"],
      frameSrc: ["https://accounts.google.com"]
    }
  }
}));

// Additional security middleware
app.use(xss());
app.use(mongoSanitize());
app.use(hpp());
app.use(securityHeaders);
app.use(sanitizeInput);
app.use(preventSQLInjection);
app.use(preventXSS);

// Rate limiting
app.use('/api/', generalLimiter);
app.use('/api/auth/', authLimiter);
app.use('/api/roll/', diceRollLimiter);

// CORS configuration with security
const corsOptions = {
  origin: process.env.FRONTEND_URL || "http://localhost:3000",
  credentials: true,
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allowedHeaders: [
    "Content-Type", 
    "Authorization", 
    "X-Requested-With",
    "X-CSRF-Token",
    "Accept",
    "Origin"
  ],
  exposedHeaders: ["X-CSRF-Token"]
};

app.use(cors(corsOptions));

// Body parsing with limits
app.use(express.json({ 
  limit: '10mb',
  // Security: Disable prototype pollution
  prototype: false
}));

app.use(express.urlencoded({ 
  extended: true, 
  limit: '10mb',
  // Security: Disable prototype pollution
  prototype: false
}));

// Routes with comprehensive security
app.get('/', (req, res) => {
  res.json({ message: 'Fate\'s Edge API Server' });
});

// Apply all security middleware to routes
app.use('/api/auth', csrfProtection, require('./routes/auth.routes'));
app.use('/api/characters', csrfProtection, require('./routes/characters.routes'));
app.use('/api/campaigns', csrfProtection, require('./routes/campaigns.routes'));
app.use('/api/roll', csrfProtection, require('./routes/roll.routes'));
app.use('/api/chat', csrfProtection, require('./routes/chat.routes'));
app.use('/api/macros', csrfProtection, require('./routes/macros.routes'));

// Socket.IO connection handling with authentication
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) {
    return next(new Error('Authentication error'));
  }
  
  // Verify the JWT token
  const jwt = require('jsonwebtoken');
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.userId = decoded.userid;
    next();
  } catch (error) {
    return next(new Error('Invalid token'));
  }
});

// Enhanced Socket.IO connection handling
io.on('connection', (socket) => {
  console.log('User connected:', socket.userId);
  
  // Store user connection
  if (socket.userId) {
    if (!activeUsers.has(socket.userId)) {
      activeUsers.set(socket.userId, new Set());
    }
    activeUsers.get(socket.userId).add(socket.id);
  }

  // Join campaign rooms with validation
  socket.on('join_campaign', (campaignId) => {
    // Validate campaign ID
    if (!campaignId || typeof campaignId !== 'string') {
      return socket.emit('error', { message: 'Invalid campaign ID' });
    }
    
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
    if (!campaignId || typeof campaignId !== 'string') {
      return;
    }
    
    socket.leave(`campaign_${campaignId}`);
    console.log(`User ${socket.userId} left campaign ${campaignId}`);
  });

  // Send chat message with validation
  socket.on('send_message', async (data) => {
    try {
      // Validate input
      if (!data || typeof data !== 'object') {
        return socket.emit('error', { message: 'Invalid message data' });
      }
      
      const { campaignId, content, channel = 'general' } = data;
      
      // Validate required fields
      if (!campaignId || !content) {
        return socket.emit('error', { message: 'Missing required fields' });
      }
      
      // Validate content length
      if (typeof content !== 'string' || content.length > 1000) {
        return socket.emit('error', { message: 'Message too long' });
      }
      
      // Validate channel
      const validChannels = ['general', 'ooc', 'private'];
      if (!validChannels.includes(channel)) {
        return socket.emit('error', { message: 'Invalid channel' });
      }
      
      // Emit message to campaign room
      const messageData = {
        campaignId,
        userId: socket.userId,
        content,
        channel,
        timestamp: new Date(),
        username: 'User_' + socket.userId.substring(0, 8) // Placeholder
      };
      
      // Emit to campaign room
      io.to(`campaign_${campaignId}`).emit('new_message', messageData);
      
    } catch (error) {
      console.error('Socket message error:', error);
      socket.emit('error', { message: 'Error sending message' });
    }
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
// backend/server.js (add to existing Socket.IO handlers)
// Execute macro
socket.on('execute_macro', async (data) => {
  try {
    const { campaignId, macroCommand, characterId } = data;
    
    // Validate input
    if (!campaignId || !macroCommand) {
      return socket.emit('error', { message: 'Missing required fields' });
    }
    
    // Get macro service
    const macroService = require('./services/macro.service');
    
    // Execute the macro
    const executionResult = await macroService.executeMacro(
      { macroCommand, characterId },
      socket.userId,
      campaignId,
      io
    );
    
    const macroResult = {
      macroCommand,
      characterId,
      userId: socket.userId,
      timestamp: new Date(),
      result: executionResult,
      username: 'User_' + socket.userId.substring(0, 8) // Placeholder
    };
    
    // Emit macro execution to campaign
    io.to(`campaign_${campaignId}`).emit('macro_executed', macroResult);
    
  } catch (error) {
    console.error('Socket macro error:', error);
    socket.emit('error', { message: 'Error executing macro' });
  }
});

});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  
  // Don't expose internal error details in production
  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({ message: 'Internal server error' });
  } else {
    res.status(500).json({ 
      message: 'Internal server error',
      error: err.message 
    });
  }
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ message: 'Route not found' });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Process terminated');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  server.close(() => {
    console.log('Process terminated');
    process.exit(0);
  });
});

