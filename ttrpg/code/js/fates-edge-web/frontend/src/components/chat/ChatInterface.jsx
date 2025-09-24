// frontend/src/components/chat/ChatInterface.jsx (updated)
import React, { useState, useEffect, useRef } from 'react';
import { useChatStore } from '../../store/chatStore';
import { useMacroStore } from '../../store/macroStore';
import { useAuthStore } from '../../store/authStore';
import socketService from '../../services/socket.service';
import ChatHeader from './ChatHeader';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import MacroPanel from '../macros/MacroPanel';

const ChatInterface = ({ campaignId, isGM }) => {
  const { messages, currentChannel, channels, initCampaignChat, error, clearError } = useChatStore();
  const { macros, getCampaignMacros } = useMacroStore();
  const { user } = useAuthStore();
  const [showMacros, setShowMacros] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Initialize chat store for campaign
        initCampaignChat(campaignId);
        
        // Join campaign via SocketIO
        socketService.joinCampaign(campaignId);
        
        // Fetch initial data
        await getCampaignMacros(campaignId);
      } catch (err) {
        console.error('Failed to initialize chat:', err);
      }
    };

    if (campaignId) {
      fetchData();
    }

    // Set up socket listeners
    const handleNewMessage = (message) => {
      useChatStore.getState().addMessage(message);
    };

    const handleUserTyping = (data) => {
      const { userId, isTyping } = data;
      useChatStore.getState().setTyping(userId, isTyping);
      useChatStore.getState().clearOldTyping();
    };

    socketService.onNewMessage(handleNewMessage);
    socketService.onUserTyping(handleUserTyping);

    // Clean up on unmount
    return () => {
      socketService.leaveCampaign(campaignId);
      socketService.removeAllListeners();
    };
  }, [campaignId, initCampaignChat, getCampaignMacros]);

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-full bg-gray-800 rounded-lg p-6">
        <div className="text-red-400 text-center">
          <h3 className="text-lg font-medium mb-2">Error loading chat</h3>
          <p className="text-sm">{error}</p>
        </div>
        <button
          onClick={clearError}
          className="mt-4 btn-primary"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-gray-800 rounded-lg shadow">
      <ChatHeader 
        campaignId={campaignId}
        currentChannel={currentChannel}
        channels={channels}
        showMacros={showMacros}
        onToggleMacros={() => setShowMacros(!showMacros)}
        isGM={isGM}
      />
      
      <div className="flex flex-1 overflow-hidden">
        {/* Main Chat Area */}
        <div className={`flex-1 flex flex-col ${showMacros ? 'hidden md:flex' : 'flex'}`}>
          <MessageList 
            messages={messages}
            currentChannel={currentChannel}
            user={user}
            messagesEndRef={messagesEndRef}
          />
          <MessageInput 
            campaignId={campaignId}
            currentChannel={currentChannel}
            user={user}
            macros={macros}
          />
        </div>
        
        {/* Macro Panel */}
        {showMacros && (
          <div className="w-full md:w-80 border-l border-gray-700">
            <MacroPanel 
              campaignId={campaignId}
              isGM={isGM}
              onClose={() => setShowMacros(false)}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;

