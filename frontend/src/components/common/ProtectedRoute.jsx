import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { LoadingPage } from './Loading';

const ProtectedRoute = ({ children, requireOrganizer = false }) => {
  const { isAuthenticated, isOrganizer, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <LoadingPage />;

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  }

  if (requireOrganizer && !isOrganizer) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;
