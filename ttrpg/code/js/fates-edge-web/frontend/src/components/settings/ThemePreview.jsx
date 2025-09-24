// frontend/src/components/settings/ThemePreview.jsx
import React from 'react';

const ThemePreview = ({ theme, isSelected, onSelect }) => {
  return (
    <div 
      className={`border-2 rounded-lg overflow-hidden cursor-pointer transition-all ${
        isSelected 
          ? 'border-fate-accent ring-2 ring-fate-accent ring-opacity-50' 
          : 'border-fate-dark hover:border-fate-accent'
      }`}
      onClick={onSelect}
    >
      <div 
        className="h-32 relative"
        style={{ backgroundColor: theme.background }}
      >
        {/* Header preview */}
        <div 
          className="h-8 flex items-center px-3"
          style={{ backgroundColor: theme.dark }}
        >
          <div className="flex space-x-1">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
        </div>
        
        {/* Content preview */}
        <div className="p-3">
          <div 
            className="h-4 rounded mb-2"
            style={{ backgroundColor: theme.dark, width: '60%' }}
          ></div>
          <div 
            className="h-3 rounded mb-1"
            style={{ backgroundColor: theme.dark, width: '80%' }}
          ></div>
          <div 
            className="h-3 rounded mb-1"
            style={{ backgroundColor: theme.dark, width: '70%' }}
          ></div>
          
          {/* Button preview */}
          <div 
            className="absolute bottom-3 right-3 h-6 rounded px-3 flex items-center text-xs"
            style={{ backgroundColor: theme.primary, color: theme.darker === '#000000' ? '#FFFFFF' : theme.darker }}
          >
            Button
          </div>
        </div>
      </div>
      
      <div 
        className="p-3 border-t"
        style={{ 
          backgroundColor: theme.darker, 
          borderColor: theme.dark,
          color: theme.text
        }}
      >
        <h3 className="font-medium">{theme.name}</h3>
      </div>
    </div>
  );
};

export default ThemePreview;

