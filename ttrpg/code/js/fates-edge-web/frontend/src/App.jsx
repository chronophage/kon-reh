import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import AuthLayout from './components/layout/AuthLayout';
import MainLayout from './components/layout/MainLayout';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './components/dashboard/Dashboard';
import CharacterSheet from './components/characters/CharacterSheet';
import CharacterList from './components/characters/CharacterList';
import CampaignDashboard from './components/campaigns/CampaignDashboard';
import DiceRoller from './components/dice/DiceRoller';
import { useAuthStore } from './store/authStore';

function App() {
  const { isAuthenticated } = useAuthStore();

  return (
    <Router>
      <div className="min-h-screen bg-fate-darker">
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
            <Route path="/characters/:id" element={isAuthenticated ? <CharacterSheet /> : <Navigate to="/login" />} />
            <Route path="/campaigns/:id" element={isAuthenticated ? <CampaignDashboard /> : <Navigate to="/login" />} />
            <Route path="/roll" element={isAuthenticated ? <DiceRoller /> : <Navigate to="/login" />} />
          </Route>

          {/* Redirect root to dashboard if authenticated */}
          <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

