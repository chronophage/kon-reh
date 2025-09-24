// frontend/src/components/macros/MacroPanel.jsx (updated)
import React, { useState } from 'react';
import { useMacroStore } from '../../store/macroStore';
import { XMarkIcon } from '@heroicons/react/24/outline';

const MacroPanel = ({ campaignId, isGM, onClose }) => {
  const { macros, executeMacro, error } = useMacroStore();
  const [selectedCharacter, setSelectedCharacter] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);

  const handleExecuteMacro = async (macroCommand) => {
    setIsExecuting(true);
    try {
      await executeMacro(campaignId, `/${macroCommand}`, selectedCharacter || null);
    } catch (error) {
      console.error('Failed to execute macro:', error);
    } finally {
      setIsExecuting(false);
    }
  };

  const publicMacros = macros.filter(macro => macro.ispublic || macro.createdby === selectedCharacter || isGM);
  const userMacros = macros.filter(macro => macro.createdby === selectedCharacter);
  const gmMacros = isGM ? macros : [];

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-4 border-b border-gray-700">
        <h2 className="text-lg font-bold text-fate-accent">Macros</h2>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-white"
        >
          <XMarkIcon className="h-5 w-5" />
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4">
        {error && (
          <div className="bg-red-900/50 border border-red-700 rounded-lg p-3 mb-4">
            <p className="text-red-200 text-sm">{error}</p>
          </div>
        )}
        
        {publicMacros.length > 0 && (
          <div className="mb-6">
            <h3 className="text-md font-medium text-fate-text mb-3">Public Macros</h3>
            <div className="space-y-2">
              {publicMacros.map(macro => (
                <button
                  key={macro.macroid}
                  onClick={() => handleExecuteMacro(macro.command)}
                  disabled={isExecuting}
                  className="w-full text-left p-3 bg-fate-dark hover:bg-fate-darker rounded-lg transition-colors disabled:opacity-50"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium text-fate-accent">/{macro.command}</div>
                      <div className="text-sm text-gray-300">{macro.name}</div>
                    </div>
                    {isExecuting && (
                      <svg className="animate-spin h-4 w-4 text-fate-accent" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    )}
                  </div>
                  {macro.description && (
                    <p className="text-xs text-gray-400 mt-1">{macro.description}</p>
                  )}
                </button>
              ))}
            </div>
          </div>
        )}
        
        {userMacros.length > 0 && (
          <div className="mb-6">
            <h3 className="text-md font-medium text-fate-text mb-3">My Macros</h3>
            <div className="space-y-2">
              {userMacros.map(macro => (
                <button
                  key={macro.macroid}
                  onClick={() => handleExecuteMacro(macro.command)}
                  disabled={isExecuting}
                  className="w-full text-left p-3 bg-fate-dark hover:bg-fate-darker rounded-lg transition-colors disabled:opacity-50"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium text-fate-accent">/{macro.command}</div>
                      <div className="text-sm text-gray-300">{macro.name}</div>
                    </div>
                  </div>
                  {macro.description && (
                    <p className="text-xs text-gray-400 mt-1">{macro.description}</p>
                  )}
                </button>
              ))}
            </div>
          </div>
        )}
        
        {isGM && gmMacros.length > 0 && (
          <div>
            <h3 className="text-md font-medium text-fate-text mb-3">GM Macros</h3>
            <div className="space-y-2">
              {gmMacros.map(macro => (
                <button
                  key={macro.macroid}
                  onClick={() => handleExecuteMacro(macro.command)}
                  disabled={isExecuting}
                  className="w-full text-left p-3 bg-fate-dark hover:bg-fate-darker rounded-lg transition-colors disabled:opacity-50"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium text-fate-accent">/{macro.command}</div>
                      <div className="text-sm text-gray-300">{macro.name}</div>
                    </div>
                  </div>
                  {macro.description && (
                    <p className="text-xs text-gray-400 mt-1">{macro.description}</p>
                  )}
                </button>
              ))}
            </div>
          </div>
        )}
        
        {macros.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <p>No macros available</p>
            <p className="text-sm mt-2">Create macros to automate common actions</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MacroPanel;

