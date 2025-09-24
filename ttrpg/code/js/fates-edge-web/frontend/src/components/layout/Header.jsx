// frontend/src/components/layout/Header.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import ThemeSelector from './ThemeSelector';
import { UserCircleIcon, ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline';

const Header = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-fate-dark border-b border-fate-darker">
      <div className="flex items-center justify-between h-16 px-4">
        <div className="flex items-center">
          <h1 
            className="text-xl font-bold cursor-pointer text-fate-accent"
            onClick={() => navigate('/dashboard')}
          >
            Fate's Edge
          </h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <ThemeSelector />
          
          <div className="relative group">
            <button className="flex items-center space-x-2 bg-fate-darker hover:bg-fate-dark rounded-lg px-3 py-2 transition-colors">
              <UserCircleIcon className="h-5 w-5 text-fate-accent" />
              <span className="text-fate-text hidden sm:inline">
                {user?.username || 'User'}
              </span>
            </button>
            
            <div className="absolute right-0 mt-2 w-48 bg-fate-dark rounded-lg shadow-lg border border-fate-darker py-1 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
              <div className="px-4 py-2 border-b border-fate-darker">
                <p className="text-sm font-medium text-fate-text">{user?.username}</p>
                <p className="text-xs text-fate-text-secondary">{user?.email}</p>
              </div>
              <button
                onClick={handleLogout}
                className="w-full flex items-center px-4 py-2 text-sm text-fate-text hover:bg-fate-darker transition-colors"
              >
                <ArrowRightOnRectangleIcon className="h-4 w-4 mr-2" />
                Sign out
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

