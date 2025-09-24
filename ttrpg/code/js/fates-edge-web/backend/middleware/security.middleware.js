// backend/middleware/security.middleware.js
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const xss = require('xss-clean');
const mongoSanitize = require('express-mongo-sanitize');
const hpp = require('hpp');

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

// Security headers middleware
const securityHeaders = (req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;");
  res.setHeader('Referrer-Policy', 'no-referrer');
  next();
};

// Input sanitization middleware
const sanitizeInput = (req, res, next) => {
  // Sanitize request body
  if (req.body) {
    for (const [key, value] of Object.entries(req.body)) {
      if (typeof value === 'string') {
        // Remove potentially dangerous characters
        req.body[key] = value
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .trim();
      }
    }
  }
  
  // Sanitize query parameters
  if (req.query) {
    for (const [key, value] of Object.entries(req.query)) {
      if (typeof value === 'string') {
        req.query[key] = value
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .trim();
      }
    }
  }
  
  next();
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
  csrfProtection
};

