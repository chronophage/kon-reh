// frontend/src/App.jsx (updated)
import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import './App.css';
import AuthLayout from './components/layout/AuthLayout';
import MainLayout from './components/layout/MainLayout';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './components/dashboard/Dashboard';
import CharacterSheet from './components/characters/CharacterSheet';
import CharacterList from './components/characters/CharacterList';
import CharacterCreator from './components/characters/CharacterCreator';
import CampaignDashboard from './components/campaigns/CampaignDashboard';
import CampaignList from './components/campaigns/CampaignList';
import CampaignCreator from './components/campaigns/CampaignCreator';
import DiceRoller from './components/dice/DiceRoller';
import MacroManager from './components/macros/MacroManager';
import SettingsPage from './components/settings/SettingsPage';
import { useAuthStore } from './store/authStore';
import { useThemeStore } from './store/themeStore';
import socketService from './services/socket.service';

function App() {
  const { isAuthenticated, user, token, verifyToken } = useAuthStore();
  const { initTheme } = useThemeStore();

  // Initialize theme on app load
  useEffect(() => {
    initTheme();
  }, [initTheme]);

  // Initialize socket connection when authenticated
  useEffect(() => {
    if (isAuthenticated && user && token) {
      socketService.connect();
    } else {
      socketService.disconnect();
    }

    // Clean up on unmount
    return () => {
      socketService.disconnect();
    };
  }, [isAuthenticated, user, token]);

  // Verify token on app load
  useEffect(() => {
    const checkAuth = async () => {
      if (token && !user) {
        await verifyToken();
      }
    };
    checkAuth();
  }, [token, user, verifyToken]);

  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <Router>
        <div className="min-h-screen bg-fate-background">
          <Routes>
            {/* Public routes */}
            <Route element={<AuthLayout />}>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
            </Route>

            {/* Protected routes */}
            <Route element={<MainLayout />}>
              <Route path="/" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
              <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
              <Route path="/characters" element={isAuthenticated ? <CharacterList /> : <Navigate to="/login" />} />
              <Route path="/characters/create" element={isAuthenticated ? <CharacterCreator /> : <Navigate to="/login" />} />
              <Route path="/characters/:id" element={isAuthenticated ? <CharacterSheet /> : <Navigate to="/login" />} />
              <Route path="/campaigns" element={isAuthenticated ? <CampaignList /> : <Navigate to="/login" />} />
              <Route path="/campaigns/create" element={isAuthenticated ? <CampaignCreator /> : <Navigate to="/login" />} />
              <Route path="/campaigns/:id" element={isAuthenticated ? <CampaignDashboard /> : <Navigate to="/login" />} />
              <Route path="/roll" element={isAuthenticated ? <DiceRoller /> : <Navigate to="/login" />} />
              <Route path="/macros" element={isAuthenticated ? <MacroManager /> : <Navigate to="/login" />} />
              <Route path="/settings" element={isAuthenticated ? <SettingsPage /> : <Navigate to="/login" />} />
            </Route>

            {/* Redirect root to dashboard if authenticated */}
            <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
          </Routes>
        </div>
      </Router>
    </GoogleOAuthProvider>
  );
}

export default App;

