/**
 * Axios API client for Venture Insight.
 * Centralized HTTP calls with JWT interceptor.
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ─── JWT Interceptor ────────────────────────────────────────

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('vi_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('vi_token');
      localStorage.removeItem('vi_email');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ─── Auth API ───────────────────────────────────────────────

export const registerUser = async (email, password) => {
  const response = await api.post('/api/register', { email, password });
  return response.data;
};

export const loginUser = async (email, password) => {
  const response = await api.post('/api/login', { email, password });
  return response.data;
};

// ─── Upload API ─────────────────────────────────────────────

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/api/upload-pdf', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// ─── Analysis API ───────────────────────────────────────────

export const analyzeStartup = async (extractedText, filename) => {
  const response = await api.post('/api/analyze', {
    extracted_text: extractedText,
    filename: filename,
  });
  return response.data;
};

export const getAnalyses = async () => {
  const response = await api.get('/api/analyses');
  return response.data;
};

export const getAnalysis = async (id) => {
  const response = await api.get(`/api/analyses/${id}`);
  return response.data;
};

// ─── Health Check ───────────────────────────────────────────

export const healthCheck = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export default api;
