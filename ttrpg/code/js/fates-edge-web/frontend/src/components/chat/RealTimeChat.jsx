// frontend/src/components/chat/RealTimeChat.jsx
import React, { useState, useEffect, useRef } from 'react';
import { useChatStore } from '../../store/chatStore';
import { useAuthStore } from '../../store/authStore';
import socketService from '../../services/socket.service';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

const RealTimeChat = ({ campaignId }) => {
  const { messages, currentChannel, addMessage, setTyping, clearOldTyping } = useChatStore();
  const { user } = useAuthStore();
  const [isTyping, setIsTyping] = useState(false);
  const [typingUsers, setTypingUsers] = useState(new Set());
  const messagesEndRef = useRef(null);

  // Join campaign on mount
  useEffect(() => {
    if (campaignId) {
      socketService.joinCampaign(campaignId);
      
      // Set up socket listeners
      socketService.onNewMessage(handleNewMessage);
      socketService.onUserTyping(handleUserTyping);
      
      // Clean up on unmount
      return () => {
        socketService.leaveCampaign(campaignId);
        socketService.removeAllListeners();
      };
    }
  }, [campaignId]);

  // Handle new messages from socket
  const handleNewMessage = (message) => {
    addMessage(message);
  };

  // Handle typing indicators from socket
  const handleUserTyping = (data) => {
    const { userId, isTyping: userIsTyping } = data;
    
    setTyping(userId, userIsTyping);
    
    setTypingUsers(prev => {
      const newSet = new Set(prev);
      if (userIsTyping) {
        newSet.add(userId);
      } else {
        newSet.delete(userId);
      }
      return newSet;
    });
    
    // Clear old typing indicators periodically
    clearOldTyping();
  };

  // Send message through socket
  const handleSendMessage = (content) => {
    if (!content.trim()) return;
    
    socketService.sendMessage({
      campaignId,
      content,
      channel: currentChannel
    });
    
    // Stop typing indicator after sending
    handleTyping(false);
  };

  // Handle typing indicator
  const handleTyping = (typing) => {
    if (typing !== isTyping) {
      setIsTyping(typing);
      socketService.sendTyping(campaignId, typing);
    }
  };

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Clean up typing indicators periodically
  useEffect(() => {
    const interval = setInterval(() => {
      clearOldTyping();
    }, 3000);
    
    return () => clearInterval(interval);
  }, [clearOldTyping]);

  // Get typing indicator text
  const getTypingText = () => {
    const typingUserIds = Array.from(typingUsers).filter(id => id !== user?.userid);
    if (typingUserIds.length === 0) return '';
    
    if (typingUserIds.length === 1) {
      return 'Someone is typing...';
    } else {
      return `${typingUserIds.length} people are typing...`;
    }
  };

  if (!campaignId) {
    return <div className="p-4 text-center text-gray-500">No campaign selected</div>;
  }

  return (
    <div className="flex flex-col h-full">
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages
          .filter(msg => msg.campaignid === campaignId && msg.channel === currentChannel)
          .map((message) => (
            <ChatMessage key={message.messageid} message={message} />
          ))}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Typing indicator */}
      {getTypingText() && (
        <div className="px-4 py-1 text-sm text-fate-accent italic">
          {getTypingText()}
        </div>
      )}
      
      {/* Input area */}
      <div className="p-4 border-t border-fate-dark">
        <ChatInput 
          onSend={handleSendMessage}
          onTyping={handleTyping}
          placeholder={`Message #${currentChannel}`}
        />
      </div>
    </div>
  );
};

export default RealTimeChat;

