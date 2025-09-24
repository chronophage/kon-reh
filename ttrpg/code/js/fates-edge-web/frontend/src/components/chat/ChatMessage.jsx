// frontend/src/components/chat/ChatMessage.jsx
import React from 'react';
import { format } from 'date-fns';

const ChatMessage = ({ message }) => {
  // Format timestamp
  const formatTime = (timestamp) => {
    try {
      return format(new Date(timestamp), 'HH:mm');
    } catch (e) {
      return 'Unknown time';
    }
  };

  // Determine message styling
  const getMessageClass = () => {
    if (message.system) return 'bg-fate-dark text-fate-accent italic';
    if (message.channel === 'private') return 'bg-fate-darker border-l-4 border-fate-accent';
    return 'bg-fate-dark';
  };

  return (
    <div className={`p-3 rounded-lg ${getMessageClass()}`}>
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-2">
          <span className="font-bold text-fate-accent">
            {message.charactername || message.username || 'Unknown User'}
          </span>
          {message.charactername && (
            <span className="text-xs text-gray-400">
              ({message.username})
            </span>
          )}
        </div>
        <span className="text-xs text-gray-500">
          {formatTime(message.timestamp)}
        </span>
      </div>
      
      <div className="mt-1 text-fate-text break-words">
        {message.content}
      </div>
      
      {message.channel === 'private' && (
        <div className="mt-1 text-xs text-fate-accent">
          Private message
        </div>
      )}
    </div>
  );
};

export default ChatMessage;

