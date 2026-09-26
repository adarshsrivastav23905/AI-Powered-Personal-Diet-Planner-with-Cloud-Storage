/**
 * API Service Layer
 * ==================
 * Centralized API communication with the Flask backend.
 * Handles authentication headers, error responses, and base URL config.
 *
 * Cloud Computing Concept: Client-Server Architecture
 * - Frontend communicates with backend through REST API
 * - All requests include JWT token for authentication
 */

import axios from 'axios';

// Base URL - configurable for different environments
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Create axios instance with defaults
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - attach JWT token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle auth errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ── Auth API ──────────────────────────────────────────────────
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  me: () => api.get('/auth/me'),
};

// ── Profile API ───────────────────────────────────────────────
export const profileAPI = {
  get: () => api.get('/profile'),
  update: (data) => api.put('/profile', data),
  getTargets: () => api.get('/profile/targets'),
};

// ── Plans API ─────────────────────────────────────────────────
export const plansAPI = {
  generate: (data) => api.post('/plans/generate', data || {}),
  getAll: () => api.get('/plans'),
  getOne: (planId) => api.get(`/plans/${planId}`),
  delete: (planId) => api.delete(`/plans/${planId}`),
};

// ── Storage API ───────────────────────────────────────────────
export const storageAPI = {
  upload: (formData) =>
    api.post('/storage/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  listFiles: () => api.get('/storage/files'),
  download: (fileId) =>
    api.get(`/storage/files/${fileId}/download`, { responseType: 'blob' }),
  delete: (fileId) => api.delete(`/storage/files/${fileId}`),
};

// ── Health Check ──────────────────────────────────────────────
export const healthCheck = () => api.get('/health');

export default api;
