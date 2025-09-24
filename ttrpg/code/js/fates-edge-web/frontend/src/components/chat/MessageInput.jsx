// frontend/src/components/chat/MessageInput.jsx (updated)
import React, { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../../store/chatStore';
import { useMacroStore } from '../../store/macroStore';
import { useCharacterStore } from '../../store/characterStore'; // Add this import
import socketService from '../../services/socket.service';
import { PaperAirplaneIcon } from '@heroicons/react/24/outline';

const MessageInput = ({ campaignId, currentChannel, user, macros }) => {
  const [message, setMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showMacroSuggestions, setShowMacroSuggestions] = useState(false);
  const [selectedCharacter, setSelectedCharacter] = useState('');
  const typingTimeoutRef = useRef(null);
  const textareaRef = useRef(null);
  const { setTyping } = useChatStore();
  const { characters } = useCharacterStore();

  // Handle typing indicators
  useEffect(() => {
    if (message.trim() && !isTyping) {
      setIsTyping(true);
      setTyping(user.userid, true);
      socketService.sendTyping(campaignId, true);
    } else if (!message.trim() && isTyping) {
      setIsTyping(false);
      setTyping(user.userid, false);
      socketService.sendTyping(campaignId, false);
    }

    // Clear typing status after delay
    if (isTyping) {
      clearTimeout(typingTimeoutRef.current);
      typingTimeoutRef.current = setTimeout(() => {
        setIsTyping(false);
        setTyping(user.userid, false);
        socketService.sendTyping(campaignId, false);
      }, 1000);
    }

    return () => {
      clearTimeout(typingTimeoutRef.current);
    };
  }, [message, isTyping, user.userid, setTyping, campaignId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    try {
      const messageData = {
        campaignId,
        content: message.trim(),
        channel: currentChannel
      };

      if (selectedCharacter) {
        messageData.characterId = selectedCharacter;
      }

      // Send message via SocketIO
      socketService.sendMessage(messageData);
      
      setMessage('');
      setShowMacroSuggestions(false);
      
      // Focus textarea after sending
      textareaRef.current?.focus();
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
    
    // Show macro suggestions when typing !
    if (e.key === '!' && message.trim() === '') {
      setShowMacroSuggestions(true);
    }
  };

  const insertMacro = (command) => {
    const newMessage = message + command + ' ';
    setMessage(newMessage);
    setShowMacroSuggestions(false);
    textareaRef.current?.focus();
  };

  // Filter macros that match current input
  const filteredMacros = macros.filter(macro => 
    macro.command.toLowerCase().includes(message.toLowerCase())
  );

  return (
    <form onSubmit={handleSubmit} className="border-t border-gray-700 p-4 bg-gray-800 rounded-b-lg">
      {/* Character selection for players */}
      {user?.role !== 'gm' && characters?.length > 0 && (
        <div className="mb-2">
          <select
            value={selectedCharacter}
            onChange={(e) => setSelectedCharacter(e.target.value)}
            className="input-field text-sm w-full"
          >
            <option value="">Send as yourself</option>
            {characters.map(character => (
              <option key={character.characterid} value={character.characterid}>
                {character.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Macro suggestions */}
      {showMacroSuggestions && filteredMacros.length > 0 && (
        <div className="mb-2 max-h-32 overflow-y-auto bg-gray-700 rounded-lg p-2">
          <div className="text-xs text-gray-400 mb-1">Available macros:</div>
          {filteredMacros.slice(0, 5).map(macro => (
            <button
              key={macro.macroid}
              type="button"
              onClick={() => insertMacro(macro.command)}
              className="block w-full text-left px-2 py-1 text-sm text-gray-300 hover:bg-gray-600 rounded"
            >
              <span className="font-mono text-purple-400">{macro.command}</span> - {macro.description || macro.name}
            </button>
          ))}
        </div>
      )}

      <div className="flex items-end space-x-2">
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={`Message #${currentChannel}...`}
            className="input-field w-full resize-none"
            rows="1"
            style={{ minHeight: '40px', maxHeight: '120px' }}
          />
          {message.trim() && (
            <div className="absolute right-2 bottom-2 text-xs text-gray-500">
              {message.length}/500
            </div>
          )}
        </div>
        
        <button
          type="submit"
          disabled={!message.trim()}
          className="p-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <PaperAirplaneIcon className="h-5 w-5" />
        </button>
      </div>
      
      <div className="flex items-center mt-2 text-xs text-gray-500">
        <span>Press Enter to send, Shift+Enter for new line</span>
        <span className="mx-2">•</span>
        <span>Type ! for macros</span>
      </div>
    </form>
  );
};

export default MessageInput;

