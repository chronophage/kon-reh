import React from 'react';
import { useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

const AuthLayout = ({ children }) => {
  const location = useLocation();
  const { isAuthenticated } = useAuthStore();

  // Redirect to dashboard if already authenticated
  if (isAuthenticated && (location.pathname === '/login' || location.pathname === '/register')) {
    window.location.href = '/dashboard';
    return null;
  }

  return (
    <div className="min-h-screen bg-fate-darker">
      {children}
    </div>
  );
};

export default AuthLayout;

