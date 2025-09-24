import React from 'react';
import { useChatStore } from '../../store/chatStore';
import { Bars3Icon, XMarkIcon, CommandLineIcon } from '@heroicons/react/24/outline';

const ChatHeader = ({ campaignId, currentChannel, channels, showMacros, onToggleMacros, isGM }) => {
  const { switchChannel } = useChatStore();

  return (
    <div className="border-b border-gray-700 bg-gray-800 rounded-t-lg">
      <div className="flex items-center justify-between p-4">
        <div className="flex items-center space-x-4">
          <h2 className="text-lg font-medium text-white">Campaign Chat</h2>
          <div className="hidden sm:flex items-center space-x-2">
            {channels.map((channel) => (
              <button
                key={channel}
                onClick={() => switchChannel(channel)}
                className={`px-3 py-1 text-sm rounded-full ${
                  currentChannel === channel
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                #{channel}
              </button>
            ))}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {isGM && (
            <button
              onClick={onToggleMacros}
              className={`p-2 rounded-lg ${
                showMacros 
                  ? 'bg-purple-600 text-white' 
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
              title="Toggle Macros"
            >
              <CommandLineIcon className="h-5 w-5" />
            </button>
          )}
          
          <button
            onClick={onToggleMacros}
            className="p-2 rounded-lg bg-gray-700 text-gray-300 hover:bg-gray-600 sm:hidden"
            title="Toggle Macros"
          >
            {showMacros ? (
              <XMarkIcon className="h-5 w-5" />
            ) : (
              <Bars3Icon className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>
      
      {/* Mobile channel selector */}
      <div className="sm:hidden px-4 pb-4">
        <select
          value={currentChannel}
          onChange={(e) => switchChannel(e.target.value)}
          className="input-field w-full"
        >
          {channels.map((channel) => (
            <option key={channel} value={channel}>
              #{channel}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default ChatHeader;

