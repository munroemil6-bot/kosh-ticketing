/**
 * Kosh Ticketing - API Service Layer
 * Centralized HTTP client with interceptors for auth tokens
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - attach auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.dispatchEvent(new Event('auth-change'));
    }
    return Promise.reject(error);
  }
);

// ==================== AUTH API ====================
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getProfile: () => api.get('/auth/me'),
  updateProfile: (data) => api.put('/auth/me', data),
};

// ==================== EVENTS API ====================
export const eventsAPI = {
  getEvents: (params = {}) => api.get('/events', { params }),
  getFeatured: () => api.get('/events/featured'),
  getCategories: () => api.get('/events/categories'),
  getEvent: (id) => api.get(`/events/${id}`),
  getRelated: (id) => api.get(`/events/${id}/related`),
  createEvent: (data) => api.post('/events', data),
};

// ==================== ORDERS API ====================
export const ordersAPI = {
  createOrder: (data) => api.post('/orders', data),
  getOrder: (id) => api.get(`/orders/${id}`),
  addAttendees: (orderId, data) => api.post(`/orders/${orderId}/attendees`, data),
  processPayment: (orderId, data) => api.post(`/orders/${orderId}/pay`, data),
  cancelOrder: (orderId) => api.post(`/orders/${orderId}/cancel`),
};

// ==================== TICKETS API ====================
export const ticketsAPI = {
  getMyTickets: () => api.get('/tickets/my-tickets'),
  getTicket: (id) => api.get(`/tickets/${id}`),
  getTicketQR: (id) => api.get(`/tickets/${id}/qr`),
  getGuestTickets: (orderNumber) => api.get(`/tickets/guest/${orderNumber}`),
};

// ==================== ADMIN API ====================
export const adminAPI = {
  getDashboard: () => api.get('/admin/dashboard'),
  getEvents: (params = {}) => api.get('/admin/events', { params }),
  getEventStats: (id) => api.get(`/admin/events/${id}/stats`),
  getEventAttendees: (id) => api.get(`/admin/events/${id}/attendees`),
  deleteEvent: (id) => api.delete(`/admin/events/${id}`),
};

export default api;
