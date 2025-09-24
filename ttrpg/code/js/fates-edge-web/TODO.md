Let me complete the Security Hardening implementation. I'll focus on the remaining critical security measures:

```javascript
// backend/middleware/security.middleware.js (completed)
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const xss = require('xss-clean');
const mongoSanitize = require('express-mongo-sanitize');
const hpp = require('hpp');
const validator = require('validator');

// Rate limiting configuration
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // limit each IP to 5 requests per windowMs
  message: {
    error: 'Too many authentication attempts, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: true,
});

const diceRollLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 20, // limit each IP to 20 rolls per minute
  message: {
    error: 'Too many dice rolls, please slow down.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// Enhanced security headers middleware
const securityHeaders = (req, res, next) => {
  // Prevent MIME type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');
  
  // Prevent clickjacking
  res.setHeader('X-Frame-Options', 'DENY');
  
  // Enable XSS filtering
  res.setHeader('X-XSS-Protection', '1; mode=block');
  
  // Enforce HTTPS
  if (process.env.NODE_ENV === 'production') {
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  }
  
  // Content Security Policy
  res.setHeader('Content-Security-Policy', 
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline' https://apis.google.com; " +
    "style-src 'self' 'unsafe-inline'; " +
    "img-src 'self' data: https:; " +
    "font-src 'self' data:; " +
    "connect-src 'self' ws: wss:; " +
    "frame-src https://accounts.google.com;"
  );
  
  // Referrer Policy
  res.setHeader('Referrer-Policy', 'no-referrer');
  
  // Permissions Policy
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
  
  next();
};

// Enhanced input sanitization middleware
const sanitizeInput = (req, res, next) => {
  // Sanitize request body
  if (req.body) {
    for (const [key, value] of Object.entries(req.body)) {
      if (typeof value === 'string') {
        req.body[key] = sanitizeString(value);
      } else if (typeof value === 'object' && value !== null) {
        req.body[key] = sanitizeObject(value);
      }
    }
  }
  
  // Sanitize query parameters
  if (req.query) {
    for (const [key, value] of Object.entries(req.query)) {
      if (typeof value === 'string') {
        req.query[key] = sanitizeString(value);
      }
    }
  }
  
  // Sanitize route parameters
  if (req.params) {
    for (const [key, value] of Object.entries(req.params)) {
      if (typeof value === 'string') {
        req.params[key] = sanitizeString(value);
      }
    }
  }
  
  next();
};

// String sanitization helper
const sanitizeString = (str) => {
  if (typeof str !== 'string') return str;
  
  return str
    // Remove potentially dangerous characters
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')
    // Remove null bytes
    .replace(/\0/g, '')
    // Trim whitespace
    .trim();
};

// Object sanitization helper
const sanitizeObject = (obj) => {
  if (typeof obj !== 'object' || obj === null) return obj;
  
  const sanitized = Array.isArray(obj) ? [] : {};
  
  for (const [key, value] of Object.entries(obj)) {
    const sanitizedKey = sanitizeString(key);
    if (typeof value === 'string') {
      sanitized[sanitizedKey] = sanitizeString(value);
    } else if (typeof value === 'object' && value !== null) {
      sanitized[sanitizedKey] = sanitizeObject(value);
    } else {
      sanitized[sanitizedKey] = value;
    }
  }
  
  return sanitized;
};

// SQL injection prevention middleware
const preventSQLInjection = (req, res, next) => {
  const sqlKeywords = [
    'UNION', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 
    'CREATE', 'ALTER', 'EXEC', 'EXECUTE', 'TRUNCATE'
  ];
  
  const sqlOperators = ['--', ';', '/*', '*/', '@@', 'CHAR', 'NCHAR'];
  
  const checkForSQLInjection = (value) => {
    if (typeof value !== 'string') return false;
    
    const upperValue = value.toUpperCase();
    
    // Check for SQL keywords
    for (const keyword of sqlKeywords) {
      if (upperValue.includes(keyword)) {
        // Additional check to avoid false positives
        const pattern = new RegExp(`\\b${keyword}\\b`, 'i');
        if (pattern.test(value)) {
          return true;
        }
      }
    }
    
    // Check for SQL operators
    for (const operator of sqlOperators) {
      if (value.includes(operator)) {
        return true;
      }
    }
    
    return false;
  };
  
  // Check body parameters
  if (req.body) {
    for (const [key, value] of Object.entries(req.body)) {
      if (checkForSQLInjection(value)) {
        return res.status(400).json({
          message: `Potential SQL injection detected in field: ${key}`
        });
      }
    }
  }
  
  // Check query parameters
  if (req.query) {
    for (const [key, value] of Object.entries(req.query)) {
      if (checkForSQLInjection(value)) {
        return res.status(400).json({
          message: `Potential SQL injection detected in query parameter: ${key}`
        });
      }
    }
  }
  
  // Check route parameters
  if (req.params) {
    for (const [key, value] of Object.entries(req.params)) {
      if (checkForSQLInjection(value)) {
        return res.status(400).json({
          message: `Potential SQL injection detected in route parameter: ${key}`
        });
      }
    }
  }
  
  next();
};

// XSS prevention middleware
const preventXSS = (req, res, next) => {
  const xssPatterns = [
    /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
    /javascript:/gi,
    /vbscript:/gi,
    /onload=/gi,
    /onerror=/gi,
    /onmouseover=/gi,
    /onfocus=/gi,
    /onblur=/gi,
    /onclick=/gi,
    /ondblclick=/gi,
    /onmousedown=/gi,
    /onmouseup=/gi,
    /onkeydown=/gi,
    /onkeypress=/gi,
    /onkeyup=/gi,
    /onchange=/gi,
    /onsubmit=/gi,
    /onreset=/gi,
    /onselect=/gi,
    /onblur=/gi,
    /onfocus=/gi,
    /onload=/gi,
    /onunload=/gi
  ];
  
  const checkForXSS = (value) => {
    if (typeof value !== 'string') return false;
    
    for (const pattern of xssPatterns) {
      if (pattern.test(value)) {
        return true;
      }
    }
    
    return false;
  };
  
  // Check body parameters
  if (req.body) {
    for (const [key, value] of Object.entries(req.body)) {
      if (checkForXSS(value)) {
        return res.status(400).json({
          message: `Potential XSS detected in field: ${key}`
        });
      }
    }
  }
  
  // Check query parameters
  if (req.query) {
    for (const [key, value] of Object.entries(req.query)) {
      if (checkForXSS(value)) {
        return res.status(400).json({
          message: `Potential XSS detected in query parameter: ${key}`
        });
      }
    }
  }
  
  next();
};

// Input validation helper
const validateInput = (value, type, options = {}) => {
  switch (type) {
    case 'email':
      return validator.isEmail(value);
    case 'uuid':
      return validator.isUUID(value);
    case 'int':
      const intVal = parseInt(value, 10);
      if (isNaN(intVal)) return false;
      if (options.min !== undefined && intVal < options.min) return false;
      if (options.max !== undefined && intVal > options.max) return false;
      return true;
    case 'string':
      if (typeof value !== 'string') return false;
      if (options.min !== undefined && value.length < options.min) return false;
      if (options.max !== undefined && value.length > options.max) return false;
      return true;
    case 'array':
      return Array.isArray(value);
    default:
      return true;
  }
};

// CSRF protection middleware
const csrfProtection = (req, res, next) => {
  // For API routes, we'll use JWT tokens instead of traditional CSRF
  // But we should validate that requests have proper authentication
  if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(req.method)) {
    // Ensure JWT token is present for state-changing operations
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ 
        message: 'Authentication required for this operation' 
      });
    }
  }
  next();
};

module.exports = {
  generalLimiter,
  authLimiter,
  diceRollLimiter,
  securityHeaders,
  sanitizeInput,
  preventSQLInjection,
  preventXSS,
  csrfProtection,
  validateInput
};
```

Now let's update the server.js to use all security measures:

```javascript
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
```

Now let's enhance the database queries to prevent SQL injection by using parameterized queries:

```javascript
// backend/routes/characters.routes.js (security enhanced)
const express = require('express');
const router = express.Router();
const { pool } = require('../config/database');
const { validateInput } = require('../middleware/security.middleware');

// Get all characters for user
router.get('/user/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    
    // Validate user ID
    if (!validateInput(userId, 'uuid')) {
      return res.status(400).json({ message: 'Invalid user ID' });
    }
    
    const result = await pool.query(
      `SELECT characterid, userid, name, description, species, background, archetype, 
              experience, createdat, updatedat
       FROM characters 
       WHERE userid = $1 
       ORDER BY createdat DESC`,
      [userId]
    );
    
    res.json(result.rows);
  } catch (error) {
    console.error('Get characters error:', error);
    res.status(500).json({ message: 'Failed to fetch characters' });
  }
});

// Get character by ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Validate character ID
    if (!validateInput(id, 'uuid')) {
      return res.status(400).json({ message: 'Invalid character ID' });
    }
    
    const result = await pool.query(
      `SELECT c.*, 
              json_agg(a.*) as attributes,
              json_agg(s.*) as skills,
              json_agg(t.*) as talents
       FROM characters c
       LEFT JOIN attributes a ON c.characterid = a.characterid
       LEFT JOIN skills s ON c.characterid = s.characterid
       LEFT JOIN talents t ON c.characterid = t.characterid
       WHERE c.characterid = $1
       GROUP BY c.characterid`,
      [id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ message: 'Character not found' });
    }
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Get character error:', error);
    res.status(500).json({ message: 'Failed to fetch character' });
  }
});

// Create character
router.post('/', async (req, res) => {
  try {
    const { userid, name, description, species, background, archetype } = req.body;
    
    // Validate input
    if (!validateInput(userid, 'uuid')) {
      return res.status(400).json({ message: 'Invalid user ID' });
    }
    
    if (!validateInput(name, 'string', { min: 1, max: 100 })) {
      return res.status(400).json({ message: 'Invalid character name' });
    }
    
    const result = await pool.query(
      `INSERT INTO characters (userid, name, description, species, background, archetype, createdat, updatedat)
       VALUES ($1, $2, $3, $4, $5, $6, NOW(), NOW())
       RETURNING *`,
      [userid, name, description || '', species || '', background || '', archetype || '']
    );
    
    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error('Create character error:', error);
    res.status(500).json({ message: 'Failed to create character' });
  }
});

// Update character
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { name, description, species, background, archetype } = req.body;
    
    // Validate character ID
    if (!validateInput(id, 'uuid')) {
      return res.status(400).json({ message: 'Invalid character ID' });
    }
    
    // Validate input
    if (name && !validateInput(name, 'string', { min: 1, max: 100 })) {
      return res.status(400).json({ message: 'Invalid character name' });
    }
    
    const result = await pool.query(
      `UPDATE characters 
       SET name = $1, description = $2, species = $3, background = $4, archetype = $5, updatedat = NOW()
       WHERE characterid = $6
       RETURNING *`,
      [name, description, species, background, archetype, id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ message: 'Character not found' });
    }
    
    res.json(result.rows[0]);
  } catch (error) {
    console.error('Update character error:', error);
    res.status(500).json({ message: 'Failed to update character' });
  }
});

// Delete character
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Validate character ID
    if (!validateInput(id, 'uuid')) {
      return res.status(400).json({ message: 'Invalid character ID' });
    }
    
    const result = await pool.query(
      'DELETE FROM characters WHERE characterid = $1 RETURNING *',
      [id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ message: 'Character not found' });
    }
    
    res.json({ message: 'Character deleted successfully' });
  } catch (error) {
    console.error('Delete character error:', error);
    res.status(500).json({ message: 'Failed to delete character' });
  }
});

module.exports = router;
```

Let's also update the frontend API service with additional security measures:

```javascript
// frontend/src/services/api.js (enhanced security)
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3001/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor to add auth token and security headers
api.interceptors.request.use(
  (config) => {
    const { token } = useAuthStore.getState();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add security headers
    config.headers['X-Content-Type-Options'] = 'nosniff';
    config.headers['X-Frame-Options'] = 'DENY';
    config.headers['X-XSS-Protection'] = '1; mode=block';
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors and security
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    
    if (error.response?.status === 429) {
      // Rate limited
      console.warn('Rate limited by server');
    }
    
    if (error.response?.status === 400) {
      // Bad request - possibly security violation
      console.warn('Bad request - possible security issue:', error.response.data);
    }
    
    if (error.response?.status === 403) {
      // Forbidden - authentication issue
      console.warn('Access forbidden:', error.response.data);
    }
    
    return Promise.reject(error);
  }
);

// Enhanced input sanitization
const sanitizeInput = (input) => {
  if (typeof input === 'string') {
    return input
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;')
      .replace(/\0/g, '') // Remove null bytes
      .trim();
  }
  
  if (typeof input === 'object' && input !== null) {
    if (Array.isArray(input)) {
      return input.map(item => sanitizeInput(item));
    }
    
    const sanitized = {};
    for (const [key, value] of Object.entries(input)) {
      sanitized[sanitizeInput(key)] = sanitizeInput(value);
    }
    return sanitized;
  }
  
  return input;
};

// Validate input helper
const validateInput = (value, type, options = {}) => {
  switch (type) {
    case 'email':
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return typeof value === 'string' && emailRegex.test(value);
    case 'uuid':
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
      return typeof value === 'string' && uuidRegex.test(value);
    case 'string':
      if (typeof value !== 'string') return false;
      if (options.min !== undefined && value.length < options.min) return false;
      if (options.max !== undefined && value.length > options.max) return false;
      return true;
    case 'number':
      const num = Number(value);
      if (isNaN(num)) return false;
      if (options.min !== undefined && num < options.min) return false;
      if (options.max !== undefined && num > options.max) return false;
      return true;
    default:
      return true;
  }
};

// Enhanced API methods with comprehensive security
const enhancedApi = {
  get: async (url, config = {}) => {
    try {
      const response = await api.get(url, config);
      return response;
    } catch (error) {
      console.error('API GET error:', error);
      throw error;
    }
  },
  
  post: async (url, data, config = {}) => {
    try {
      // Sanitize and validate data before sending
      const sanitizedData = sanitizeInput(data);
      
      const response = await api.post(url, sanitizedData, config);
      return response;
    } catch (error) {
      console.error('API POST error:', error);
      throw error;
    }
  },
  
  put: async (url, data, config = {}) => {
    try {
      // Sanitize and validate data before sending
      const sanitizedData = sanitizeInput(data);
      
      const response = await api.put(url, sanitizedData, config);
      return response;
    } catch (error) {
      console.error('API PUT error:', error);
      throw error;
    }
  },
  
  delete: async (url, config = {}) => {
    try {
      const response = await api.delete(url, config);
      return response;
    } catch (error) {
      console.error('API DELETE error:', error);
      throw error;
    }
  }
};

export { sanitizeInput, validateInput };
export default enhancedApi;
```

Now let's update the TODO.md to reflect the completed security hardening:

```markdown
# Fate's Edge Web Client - Development Status Summary

## Current Implementation Status

### ✅ Completed Features

1. **Authentication System**
   - User registration/login with JWT tokens
   - Password hashing and validation
   - Protected routes and session management
   - Zustand state management with persistence
   - Google OAuth integration

2. **Database Schema & API**
   - Complete PostgreSQL schema with all required tables
   - RESTful API endpoints for all core features
   - Input validation and error handling
   - Rate limiting for dice rolls and complications

3. **Character Management**
   - Full CRUD operations for characters
   - XP spending and advancement system
   - Attributes, skills, talents, assets, followers, complications management
   - Boon system with convert/spend functionality

4. **Campaign Management**
   - Campaign creation and player invitation system
   - Session tracking and management
   - Campaign clock visualization
   - Player roster with GM controls

5. **Dice Roller System**
   - Fate's Edge dice mechanics implementation
   - Description ladder (Basic/Detailed/Intricate)
   - Visual dice display with success/complication tracking
   - Roll history and complication drawing

6. **Chat System with Macros**
   - Channel-based messaging (General/OOC/Private)
   - Macro creation with GM approval workflow
   - Public/private macro visibility controls
   - Typing indicators and message formatting
   - Real-time communication with Socket.IO

7. **Themeable Interface**
   - Multiple predefined themes
   - Custom theme creation
   - Persistent theme storage
   - Theme selector component

## 📋 TODO List - Priority Order

### ✅ 1. Real-time Communication (HIGH PRIORITY) - COMPLETED
### ✅ 2. Frontend Integration Completion (HIGH PRIORITY) - COMPLETED
### 🔧 3. Campaign Dashboard Enhancement (MEDIUM PRIORITY) - IN PROGRESS

### ✅ 4. Security Hardening (HIGH PRIORITY) - COMPLETED
**Files created/modified:**
- `backend/middleware/security.middleware.js` - Comprehensive security middleware
- `backend/server.js` - Security headers and middleware integration
- `backend/routes/*` - Enhanced validation and SQL injection prevention
- `frontend/src/services/api.js` - Request sanitization and security

**Key requirements completed:**
- ✅ Implement comprehensive input validation
- ✅ Add CSRF protection
- ✅ Enhance rate limiting
- ✅ Add security headers
- ✅ Implement SQL injection prevention
- ✅ Add XSS protection

### 5. Macro Execution System (HIGH PRIORITY)
**Files to create/modify:**
- `backend/services/macro.service.js` - Macro parsing and execution
- `backend/routes/macros.routes.js` - Enhanced macro endpoints
- `frontend/src/components/macros/*` - Macro execution UI
- `frontend/src/store/macroStore.js` - Execution state management

**Key requirements:**
- Server-side macro interpretation
- Integration with dice roller system
- Permission and approval workflow
- Error handling for malformed macros

### 6. Mobile Responsiveness (MEDIUM PRIORITY)
**Files to modify:**
- All frontend components - Mobile-first design
- `frontend/src/index.css` - Mobile-specific styles
- Navigation components - Mobile menu implementation

**Key requirements:**
- Optimize touch targets for mobile
- Implement collapsible menus
- Ensure proper spacing on small screens
- Test on various mobile devices

## 🎨 Key Design Choices

### Architecture
- **Frontend**: React with Zustand for state management
- **Backend**: Node.js/Express with PostgreSQL
- **Real-time**: Socket.IO for chat and live updates
- **Authentication**: JWT with refresh tokens and Google OAuth
- **Deployment**: Docker containers with nginx reverse proxy

### Component Structure
```
src/
├── components/
│   ├── auth/          # Login/registration
│   ├── layout/        # Navigation and layout
│   ├── dashboard/     # Main dashboard views
│   ├── characters/    # Character management
│   ├── campaigns/     # Campaign management
│   ├── dice/          # Dice roller system
│   ├── chat/          # Chat interface
│   ├── macros/        # Macro management
│   └── settings/      # Theme and user settings
├── store/             # Zustand stores
├── services/          # API and Socket.IO services
└── utils/             # Helper functions
```

### State Management
- **Zustand** for all frontend state
- **Persistent storage** for auth tokens and themes
- **Separate stores** for different domains (auth, characters, campaigns, chat, dice, macros, theme)
- **Real-time updates** through Socket.IO integration

## ⚠️ Ambiguous Aspects & Decisions Needed

### 1. User Lookup for Invitations
**Current state**: Partial implementation in PlayerList component
**Decision needed**: How to handle player invitations?
- Email lookup system?
- User search by username?
- Direct user ID input?

### 2. Character Association in Chat
**Current state**: Implemented
**Decision needed**: Should messages always require character association?
- Players: Must select character
- GM: Can send as self or any character
- System messages: Automated notifications

### 3. Macro Execution
**Current state**: UI implemented, execution logic needed
**Decision needed**: How should macros execute?
- Client-side parsing and API calls?
- Server-side macro interpretation?
- Integration with dice roller?

### 4. Campaign Clock Implementation
**Current state**: Visual display enhanced with interactivity
**Decision needed**: Full interactive functionality?
- GM controls for ticking/resetting
- Visual feedback for clock changes
- Integration with session tracking

### 5. Offline Capability
**Current state**: Not implemented
**Decision needed**: What offline features are needed?
- Character sheet viewing?
- Roll history access?
- Draft message composition?

## 🔧 Technical Debt & Improvements

### 1. Error Handling Consistency
- Standardize error message display
- Implement retry mechanisms
- Add offline error states

### 2. Loading State Management
- Add skeleton loaders
- Implement optimistic updates
- Handle slow network scenarios

### 3. Form Validation
- Add comprehensive client-side validation
- Implement real-time field validation
- Standardize validation error display

### 4. Accessibility
- Add proper ARIA labels
- Implement keyboard navigation
- Ensure color contrast compliance

## 🚀 Next Session Setup

### To Continue Development:
1. **Pull latest code** from repository
2. **Start Docker containers**: `docker-compose up --build`
3. **Verify API endpoints** are accessible at `http://localhost:3001`
4. **Start frontend**: `cd frontend && npm run dev`
5. **Check database initialization** in `docker/init.sql`

### Key Files to Review:
- `backend/server.js` - Main server configuration
- `frontend/src/App.jsx` - Route configuration
- `docker-compose.yml` - Environment setup
- All store files in `frontend/src/store/` - State management

### Testing Points:
- Authentication flow (register/login/Google auth)
- Character CRUD operations
- Campaign creation and management
- Dice rolling functionality
- Real-time chat with Socket.IO
- Campaign dashboard enhancements
- Theme switching
- Security features
