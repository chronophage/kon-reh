// frontend/src/components/chat/ChatInterface.jsx
import React, { useState, useEffect, useRef } from 'react';
import ChatHeader from './ChatHeader';
import MessageList from './MessageList';
import { useChatStore } from '../../store/chatStore';
import { useAuthStore } from '../../store/authStore';

const ChatInterface = ({ campaignId }) => {
  const { user } = useAuthStore();
  const { messages, sendMessage, joinChannel, currentChannel } = useChatStore();
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (campaignId) {
      joinChannel(campaignId);
    }
  }, [campaignId, joinChannel]);

  const handleSend = (e) => {
    e.preventDefault();
    if (inputText.trim() && user) {
      sendMessage({
        channelId: campaignId,
        userId: user.userId,
        username: user.username,
        content: inputText,
        timestamp: new Date()
      });
      setInputText('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend(e);
    }
  };

  return (
    <div className="flex flex-col h-full bg-fate-dark border border-fate-accent rounded-lg">
      <ChatHeader campaignId={campaignId} />
      
      <div className="flex-1 overflow-y-auto p-4">
        <MessageList messages={messages} currentUserId={user?.userId} />
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSend} className="border-t border-fate-accent p-3">
        <div className="flex">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type a message or use macros (!roll, !sheet, etc.)"
            className="flex-1 bg-fate-darker text-white rounded-l-lg p-2 border border-fate-accent focus:outline-none focus:ring-2 focus:ring-fate-accent"
            rows="2"
          />
          <button
            type="submit"
            className="bg-fate-accent hover:bg-fate-primary text-white font-bold py-2 px-4 rounded-r-lg transition duration-200"
          >
            Send
          </button>
        </div>
        <div className="text-xs text-fate-muted mt-1">
          Press Enter to send, Shift+Enter for new line
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;

