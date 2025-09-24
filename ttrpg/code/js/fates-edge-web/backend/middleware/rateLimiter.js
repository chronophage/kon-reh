const rateLimit = require('express-rate-limit');

// Rate limiter for dice rolls - 30 rolls per minute per user
exports.rollLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 30,
  message: {
    message: 'Too many dice rolls from this IP, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// Rate limiter for complication draws - 10 per minute per user
exports.complicationLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 10,
  message: {
    message: 'Too many complication draws from this IP, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

