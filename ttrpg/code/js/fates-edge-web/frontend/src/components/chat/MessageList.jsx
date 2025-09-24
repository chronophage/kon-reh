import React from 'react';
import { useChatStore } from '../../store/chatStore';
import MessageItem from './MessageItem';

const MessageList = ({ messages, currentChannel, user, messagesEndRef }) => {
  const { typingUsers } = useChatStore();

  // Filter messages by current channel
  const channelMessages = messages.filter(msg => msg.channel === currentChannel);

  // Get typing users for current channel
  const typingUsersList = Array.from(typingUsers.keys()).filter(userId => userId !== user?.userid);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {channelMessages.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-full text-gray-500">
          <svg className="h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <p>No messages yet. Be the first to send a message!</p>
        </div>
      ) : (
        <>
          {channelMessages.map((message) => (
            <MessageItem 
              key={message.messageid} 
              message={message} 
              currentUser={user} 
            />
          ))}
        </>
      )}
      
      {/* Typing indicators */}
      {typingUsersList.length > 0 && (
        <div className="flex items-center text-sm text-gray-400">
          <div className="flex space-x-1">
            {typingUsersList.slice(0, 3).map((_, index) => (
              <div
                key={index}
                className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                style={{ animationDelay: `${index * 0.2}s` }}
              />
            ))}
          </div>
          <span className="ml-2">
            {typingUsersList.length === 1 ? 'Someone is typing...' : `${typingUsersList.length} people are typing...`}
          </span>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;

