/**
 * Kosh Ticketing - Utility Functions
 * Formatting, helpers, and common utilities
 */

import { format, parseISO, isPast, isFuture, differenceInDays } from 'date-fns';

// ==================== DATE FORMATTING ====================
export const formatDate = (dateString, formatStr = 'MMM d, yyyy') => {
  if (!dateString) return 'TBD';
  try {
    return format(parseISO(dateString), formatStr);
  } catch {
    return dateString;
  }
};

export const formatDateTime = (dateString) => {
  if (!dateString) return 'TBD';
  try {
    return format(parseISO(dateString), 'EEE, MMM d, yyyy • h:mm a');
  } catch {
    return dateString;
  }
};

export const formatTime = (dateString) => {
  if (!dateString) return '';
  try {
    return format(parseISO(dateString), 'h:mm a');
  } catch {
    return '';
  }
};

export const getDaysUntil = (dateString) => {
  if (!dateString) return null;
  try {
    const days = differenceInDays(parseISO(dateString), new Date());
    if (days < 0) return 'Past';
    if (days === 0) return 'Today';
    if (days === 1) return 'Tomorrow';
    return `${days} days`;
  } catch {
    return null;
  }
};

// ==================== CURRENCY FORMATTING ====================
export const formatCurrency = (amount, currency = 'USD') => {
  if (amount === null || amount === undefined) return '$0.00';
  const symbols = { USD: '$', EUR: '€', GBP: '£' };
  const symbol = symbols[currency] || '$';
  return `${symbol}${parseFloat(amount).toFixed(2)}`;
};

// ==================== CATEGORY ICONS & COLORS ====================
export const categoryConfig = {
  concert: { label: 'Concerts', color: 'from-pink-500 to-rose-500', bg: 'bg-pink-500/20', text: 'text-pink-400' },
  theatre: { label: 'Theatre', color: 'from-amber-500 to-orange-500', bg: 'bg-amber-500/20', text: 'text-amber-400' },
  festival: { label: 'Festivals', color: 'from-violet-500 to-purple-500', bg: 'bg-violet-500/20', text: 'text-violet-400' },
  sports: { label: 'Sports', color: 'from-emerald-500 to-teal-500', bg: 'bg-emerald-500/20', text: 'text-emerald-400' },
  comedy: { label: 'Comedy', color: 'from-yellow-500 to-amber-500', bg: 'bg-yellow-500/20', text: 'text-yellow-400' },
  exhibition: { label: 'Exhibitions', color: 'from-cyan-500 to-blue-500', bg: 'bg-cyan-500/20', text: 'text-cyan-400' },
  workshop: { label: 'Workshops', color: 'from-indigo-500 to-blue-500', bg: 'bg-indigo-500/20', text: 'text-indigo-400' },
  other: { label: 'Other', color: 'from-gray-500 to-slate-500', bg: 'bg-gray-500/20', text: 'text-gray-400' },
};

export const getCategoryConfig = (category) => {
  return categoryConfig[category?.toLowerCase()] || categoryConfig.other;
};

// ==================== STATUS HELPERS ====================
export const getEventStatus = (event) => {
  if (event.is_sold_out) return { label: 'Sold Out', color: 'text-red-400 bg-red-500/20' };
  if (event.status === 'on_sale') return { label: 'On Sale', color: 'text-emerald-400 bg-emerald-500/20' };
  if (event.status === 'sold_out') return { label: 'Sold Out', color: 'text-red-400 bg-red-500/20' };
  return { label: 'Coming Soon', color: 'text-kosh-400 bg-kosh-500/20' };
};

// ==================== VALIDATION ====================
export const validateEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

export const validatePhone = (phone) => {
  return /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/.test(phone);
};

// ==================== LOCAL STORAGE ====================
export const storage = {
  get: (key) => {
    try {
      return JSON.parse(localStorage.getItem(key));
    } catch {
      return localStorage.getItem(key);
    }
  },
  set: (key, value) => localStorage.setItem(key, JSON.stringify(value)),
  remove: (key) => localStorage.removeItem(key),
};

// ==================== SCROLL HELPERS ====================
export const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// ==================== DEBOUNCE ====================
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};
