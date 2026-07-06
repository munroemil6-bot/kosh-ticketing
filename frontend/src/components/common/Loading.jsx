/**
 * Kosh Ticketing - Loading Component
 * Animated loading states
 */

import React from 'react';
import { Ticket } from 'lucide-react';

export const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizes = { sm: 'w-5 h-5', md: 'w-8 h-8', lg: 'w-12 h-12', xl: 'w-16 h-16' };

  return (
    <div className={`animate-spin ${sizes[size]} ${className}`}>
      <Ticket className="w-full h-full text-kosh-500" />
    </div>
  );
};

export const LoadingPage = () => (
  <div className="min-h-screen flex flex-col items-center justify-center bg-dark-900">
    <div className="relative">
      <div className="absolute inset-0 bg-kosh-500/20 blur-2xl rounded-full animate-pulse" />
      <LoadingSpinner size="xl" />
    </div>
    <p className="mt-4 text-gray-400 animate-pulse">Loading amazing events...</p>
  </div>
);

export const LoadingCard = () => (
  <div className="glass-card overflow-hidden animate-pulse">
    <div className="aspect-[16/10] bg-white/5" />
    <div className="p-4 space-y-3">
      <div className="h-4 bg-white/5 rounded w-3/4" />
      <div className="h-3 bg-white/5 rounded w-1/2" />
      <div className="flex justify-between items-center pt-2">
        <div className="h-6 bg-white/5 rounded w-20" />
        <div className="h-8 bg-white/5 rounded w-24" />
      </div>
    </div>
  </div>
);

export default LoadingSpinner;
