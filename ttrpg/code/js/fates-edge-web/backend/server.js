// backend/server.js (updated security section)
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
  csrfProtection 
} = require('./middleware/security.middleware');

dotenv.config();

const app = express();
const server = http.createServer(app);
const PORT = process.env.PORT || 3001;

// Store active users and sockets
const activeUsers = new Map();

// Security middleware
app.use(helmet());
app.use(xss());
app.use(mongoSanitize());
app.use(hpp());
app.use(securityHeaders);
app.use(sanitizeInput);

// Rate limiting
app.use('/api/', generalLimiter);
app.use('/api/auth/', authLimiter);
app.use('/api/roll/', diceRollLimiter);

// CORS configuration
app.use(cors({
  origin: process.env.FRONTEND_URL || "http://localhost:3000",
  credentials: true,
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization", "X-Requested-With"]
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Store io instance for use in routes
app.set('io', io);

// Routes with CSRF protection
app.get('/', (req, res) => {
  res.json({ message: 'Fate\'s Edge API Server' });
});

// Apply CSRF protection to state-changing routes
app.use('/api/auth', csrfProtection, require('./routes/auth.routes'));
app.use('/api/characters', csrfProtection, require('./routes/characters.routes'));
app.use('/api/campaigns', csrfProtection, require('./routes/campaigns.routes'));
app.use('/api/roll', csrfProtection, require('./routes/roll.routes'));
app.use('/api/chat', csrfProtection, require('./routes/chat.routes'));
app.use('/api/macros', csrfProtection, require('./routes/macros.routes'));

