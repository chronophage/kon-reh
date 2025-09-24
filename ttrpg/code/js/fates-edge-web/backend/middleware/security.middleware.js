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

