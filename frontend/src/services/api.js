import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
});

API.interceptors.request.use((req) => {
  const token = localStorage.getItem('token');
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

export const loginUser = (data) => 
  API.post('/auth/login/', data);

export const registerUser = (data) => 
  API.post('/auth/register/', data);

export const getDashboardStats = () => 
  API.get('/user/progress/');

export const getRecentSessions = () => 
  API.get('/interviews/sessions/');

export const startInterview = (data) => 
  API.post('/interviews/start/', data);

export const getReport = (id) => 
  API.get(`/interviews/report/${id}/`);