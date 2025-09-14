import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API functions
export const authAPI = {
  login: (credentials) => api.post('/token/', credentials),
  refresh: (refreshToken) => api.post('/token/refresh/', { refresh: refreshToken }),
};

export const candidatesAPI = {
  getCandidates: () => api.get('/candidates/'),
};

export const voteAPI = {
  castVote: (candidateId) => api.post('/vote/', { candidate: candidateId }),
};

export const resultsAPI = {
  getResults: () => api.get('/results/'),
};

export default api;
