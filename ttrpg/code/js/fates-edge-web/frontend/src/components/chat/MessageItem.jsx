import React from 'react';

const MessageItem = ({ message, currentUser }) => {
  const isOwnMessage = message.userid === currentUser?.userid;
  const isWhisper = message.channel === 'private';
  const isGM = currentUser?.role === 'gm';

  // Parse macro commands in message
  const parseMessageContent = (content) => {
    // Simple macro detection
    if (content.startsWith('!')) {
      return (
        <span className="inline-flex items-center px-2 py-1 bg-purple-900 text-purple-200 text-xs rounded">
          <CommandLineIcon className="h-3 w-3 mr-1" />
          {content}
        </span>
      );
    }
    return content;
  };

  const CommandLineIcon = () => (
    <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
    </svg>
  );

  return (
    <div className={`flex ${isOwnMessage ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-xs sm:max-w-md lg:max-w-lg xl:max-w-xl rounded-lg p-3 ${
        isOwnMessage 
          ? 'bg-purple-600 text-white' 
          : isWhisper 
            ? 'bg-yellow-900 text-yellow-100 border-l-4 border-yellow-500' 
            : 'bg-gray-700 text-white'
      }`}>
        <div className="flex items-center mb-1">
          <span className="text-xs font-medium">
            {message.charactername || message.username}
          </span>
          {isWhisper && (
            <span className="ml-2 text-xs bg-yellow-800 text-yellow-200 px-1.5 py-0.5 rounded">
              Whisper
            </span>
          )}
          {isGM && message.userid !== currentUser?.userid && (
            <span className="ml-2 text-xs bg-blue-800 text-blue-200 px-1.5 py-0.5 rounded">
              Player
            </span>
          )}
        </div>
        <div className="text-sm">
          {parseMessageContent(message.content)}
        </div>
        <div className="text-xs opacity-70 mt-1">
          {new Date(message.createdat).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </div>
      </div>
    </div>
  );
};

export default MessageItem;

