// frontend/src/components/layout/ThemeSelector.jsx
import React, { useState } from 'react';
import { useThemeStore, themes } from '../../store/themeStore';
import { SunIcon, MoonIcon, SwatchIcon } from '@heroicons/react/24/outline';

const ThemeSelector = () => {
  const { currentTheme, setTheme, themes: availableThemes } = useThemeStore();
  const [isOpen, setIsOpen] = useState(false);

  const handleThemeChange = (themeName) => {
    setTheme(themeName);
    setIsOpen(false);
  };

  const getThemePreview = (theme) => {
    return {
      background: theme.background,
      primary: theme.primary,
      text: theme.text
    };
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-center w-10 h-10 rounded-full bg-fate-dark hover:bg-fate-darker text-fate-text transition-colors"
        aria-label="Select theme"
      >
        <SwatchIcon className="h-5 w-5" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-fate-dark rounded-lg shadow-lg border border-fate-darker z-50">
          <div className="p-3 border-b border-fate-darker">
            <h3 className="text-sm font-medium text-fate-text">Choose Theme</h3>
          </div>
          
          <div className="max-h-64 overflow-y-auto">
            {Object.entries(availableThemes).map(([key, theme]) => {
              const preview = getThemePreview(theme);
              return (
                <button
                  key={key}
                  onClick={() => handleThemeChange(key)}
                  className={`w-full flex items-center p-3 text-left hover:bg-fate-darker transition-colors ${
                    currentTheme === key ? 'bg-fate-darker' : ''
                  }`}
                >
                  <div 
                    className="w-8 h-8 rounded-md border border-fate-dark flex items-center justify-center mr-3"
                    style={{ backgroundColor: preview.background }}
                  >
                    <div 
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: preview.primary }}
                    />
                  </div>
                  <span className="text-fate-text">{theme.name}</span>
                  {currentTheme === key && (
                    <svg className="ml-auto h-5 w-5 text-fate-accent" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
              );
            })}
          </div>
          
          <div className="p-3 border-t border-fate-darker text-xs text-fate-text-secondary">
            <p>Themes update the entire interface color scheme</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ThemeSelector;

