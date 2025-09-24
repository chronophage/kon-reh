// frontend/src/components/settings/SettingsPage.jsx
import React, { useState } from 'react';
import { useThemeStore, themes } from '../../store/themeStore';
import ThemePreview from './ThemePreview';

const SettingsPage = () => {
  const { currentTheme, setTheme, themes: availableThemes } = useThemeStore();
  const [newTheme, setNewTheme] = useState({
    name: '',
    primary: '#8B5CF6',
    secondary: '#7C3AED',
    accent: '#A78BFA',
    background: '#111827',
    darker: '#0F172A',
    dark: '#1E293B',
    text: '#F1F5F9',
    textSecondary: '#94A3B8'
  });

  const handleThemeSelect = (themeName) => {
    setTheme(themeName);
  };

  const handleCustomThemeChange = (field, value) => {
    setNewTheme({
      ...newTheme,
      [field]: value
    });
  };

  const handleCreateCustomTheme = () => {
    if (!newTheme.name.trim()) return;
    
    useThemeStore.getState().createCustomTheme(newTheme.name, newTheme);
    setTheme(newTheme.name);
  };

  return (
    <div className="p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-fate-accent mb-6">Settings</h1>
        
        <div className="bg-fate-dark rounded-lg p-6 mb-6">
          <h2 className="text-xl font-bold text-fate-accent mb-4">Appearance</h2>
          
          <div className="mb-6">
            <h3 className="text-lg font-medium text-fate-text mb-3">Theme</h3>
            <p className="text-fate-text-secondary text-sm mb-4">
              Choose a theme for the application interface
            </p>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {Object.entries(availableThemes).map(([key, theme]) => (
                <ThemePreview
                  key={key}
                  theme={theme}
                  isSelected={currentTheme === key}
                  onSelect={() => handleThemeSelect(key)}
                />
              ))}
            </div>
          </div>
          
          <div className="border-t border-fate-darker pt-6">
            <h3 className="text-lg font-medium text-fate-text mb-3">Custom Theme</h3>
            <p className="text-fate-text-secondary text-sm mb-4">
              Create your own color scheme
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-fate-text mb-2">
                  Theme Name
                </label>
                <input
                  type="text"
                  value={newTheme.name}
                  onChange={(e) => handleCustomThemeChange('name', e.target.value)}
                  className="input-field w-full"
                  placeholder="Enter theme name"
                />
              </div>
              
              {Object.entries(newTheme).filter(([key]) => key !== 'name').map(([key, value]) => (
                <div key={key}>
                  <label className="block text-sm font-medium text-fate-text mb-2 capitalize">
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </label>
                  <div className="flex items-center">
                    <input
                      type="color"
                      value={value}
                      onChange={(e) => handleCustomThemeChange(key, e.target.value)}
                      className="w-10 h-10 border-0 rounded cursor-pointer"
                    />
                    <input
                      type="text"
                      value={value}
                      onChange={(e) => handleCustomThemeChange(key, e.target.value)}
                      className="input-field ml-2 flex-1"
                    />
                  </div>
                </div>
              ))}
            </div>
            
            <button
              onClick={handleCreateCustomTheme}
              disabled={!newTheme.name.trim()}
              className="btn-primary mt-4"
            >
              Create Custom Theme
            </button>
          </div>
        </div>
        
        <div className="bg-fate-dark rounded-lg p-6">
          <h2 className="text-xl font-bold text-fate-accent mb-4">Current Theme Preview</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-fate-background p-4 rounded-lg">
              <h3 className="font-medium mb-2">Background</h3>
              <div className="text-fate-text-secondary text-sm">Primary content area</div>
            </div>
            <div className="bg-fate-dark p-4 rounded-lg">
              <h3 className="font-medium mb-2">Dark Panel</h3>
              <div className="text-fate-text-secondary text-sm">Secondary panels</div>
            </div>
            <div className="bg-fate-darker p-4 rounded-lg">
              <h3 className="font-medium mb-2">Darker Panel</h3>
              <div className="text-fate-text-secondary text-sm">Emphasis areas</div>
            </div>
          </div>
          
          <div className="flex space-x-4 mt-4">
            <button className="btn-primary">Primary Button</button>
            <button className="btn-secondary">Secondary Button</button>
            <button className="btn-accent">Accent Button</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;

