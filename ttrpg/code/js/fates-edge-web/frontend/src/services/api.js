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

