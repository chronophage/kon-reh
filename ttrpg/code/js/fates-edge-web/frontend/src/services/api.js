// frontend/src/services/api.js
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3001/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const { token } = useAuthStore.getState();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
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
    
    return Promise.reject(error);
  }
);

// Sanitize input helper
const sanitizeInput = (input) => {
  if (typeof input === 'string') {
    return input
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .trim();
  }
  return input;
};

// Enhanced API methods with input sanitization
const enhancedApi = {
  get: (url, config = {}) => api.get(url, config),
  
  post: (url, data, config = {}) => {
    // Sanitize data before sending
    const sanitizedData = {};
    for (const [key, value] of Object.entries(data || {})) {
      sanitizedData[key] = sanitizeInput(value);
    }
    return api.post(url, sanitizedData, config);
  },
  
  put: (url, data, config = {}) => {
    // Sanitize data before sending
    const sanitizedData = {};
    for (const [key, value] of Object.entries(data || {})) {
      sanitizedData[key] = sanitizeInput(value);
    }
    return api.put(url, sanitizedData, config);
  },
  
  delete: (url, config = {}) => api.delete(url, config)
};

export default enhancedApi;

