import React, { useState } from 'react';
import { ClockIcon, PlusIcon } from '@heroicons/react/24/outline';

const CampaignClocks = ({ campaign, isGM }) => {
  const [clocks] = useState([
    { id: 1, name: 'Mandate', progress: 3, total: 8, description: 'Political pressure builds' },
    { id: 2, name: 'Crisis', progress: 5, total: 8, description: 'Emerging threat' },
    { id: 3, name: 'Primary Goal', progress: 2, total: 6, description: 'Main storyline' }
  ]);

  const ClockDisplay = ({ clock }) => {
    const percentage = (clock.progress / clock.total) * 100;
    const segments = Array.from({ length: clock.total }, (_, i) => i);

    return (
      <div className="bg-gray-700 rounded-lg p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-medium text-white">{clock.name}</h3>
          <span className="text-sm text-gray-400">{clock.progress}/{clock.total}</span>
        </div>
        <p className="text-sm text-gray-300 mb-3">{clock.description}</p>
        
        <div className="flex justify-center">
          <div className="relative w-32 h-32">
            <svg className="w-full h-full" viewBox="0 0 100 100">
              {/* Background circle */}
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="#374151"
                strokeWidth="8"
              />
              
              {/* Progress segments */}
              {segments.map((segment, index) => {
                const angle = (360 / clock.total) * index - 90;
                const isActive = index < clock.progress;
                const strokeColor = isActive ? '#8b5cf6' : '#374151';
                
                return (
                  <line
                    key={segment}
                    x1="50"
                    y1="5"
                    x2="50"
                    y2="15"
                    stroke={strokeColor}
                    strokeWidth="2"
                    transform={`rotate(${angle} 50 50)`}
                  />
                );
              })}
              
              {/* Progress arc */}
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="#8b5cf6"
                strokeWidth="8"
                strokeDasharray={`${percentage * 2.83} 283`}
                transform="rotate(-90 50 50)"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-xl font-bold text-white">{clock.progress}</span>
            </div>
          </div>
        </div>
        
        {isGM && (
          <div className="mt-3 flex space-x-2">
            <button className="flex-1 btn-secondary text-xs py-1">
              + Tick
            </button>
            <button className="flex-1 btn-danger text-xs py-1">
              Reset
            </button>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="bg-gray-800 rounded-lg shadow">
      <div className="px-4 py-5 sm:px-6 border-b border-gray-700">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-medium text-white">Campaign Clocks</h2>
          {isGM && (
            <button className="btn-secondary flex items-center text-sm">
              <PlusIcon className="h-4 w-4 mr-1" />
              Add Clock
            </button>
          )}
        </div>
      </div>
      <div className="p-6">
        {clocks.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {clocks.map(clock => (
              <ClockDisplay key={clock.id} clock={clock} />
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <ClockIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-200">No clocks</h3>
            <p className="mt-1 text-sm text-gray-400">
              {isGM 
                ? 'Create your first campaign clock to track story progression.' 
                : 'Your GM hasn\'t created any campaign clocks yet.'}
            </p>
            {isGM && (
              <div className="mt-6">
                <button className="btn-primary inline-flex items-center">
                  <PlusIcon className="h-4 w-4 mr-1" />
                  Add Clock
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CampaignClocks;

