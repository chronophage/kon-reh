// frontend/src/components/chat/ChatInput.jsx
import React, { useState, useRef } from 'react';

const ChatInput = ({ onSend, onTyping, placeholder = "Type a message..." }) => {
  const [message, setMessage] = useState('');
  const typingTimeoutRef = useRef(null);

  const handleSend = () => {
    if (message.trim()) {
      onSend(message.trim());
      setMessage('');
      
      // Clear typing indicator
      if (onTyping) {
        onTyping(false);
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setMessage(value);
    
    // Handle typing indicators
    if (onTyping) {
      if (value.trim()) {
        // User started typing
        onTyping(true);
        
        // Reset the typing timeout
        if (typingTimeoutRef.current) {
          clearTimeout(typingTimeoutRef.current);
        }
        
        // Set timeout to stop typing indicator after pause
        typingTimeoutRef.current = setTimeout(() => {
          onTyping(false);
        }, 1000);
      } else {
        // User cleared input
        onTyping(false);
      }
    }
  };

  return (
    <div className="flex items-end space-x-2">
      <div className="flex-1">
        <textarea
          value={message}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          className="w-full bg-fate-dark text-fate-text rounded-lg p-3 resize-none focus:outline-none focus:ring-2 focus:ring-fate-accent"
          rows="2"
        />
      </div>
      <button
        onClick={handleSend}
        disabled={!message.trim()}
        className="bg-fate-accent hover:bg-fate-primary text-fate-darker font-bold py-2 px-4 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Send
      </button>
    </div>
  );
};

export default ChatInput;

