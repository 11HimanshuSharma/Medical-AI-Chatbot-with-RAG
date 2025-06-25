import React, { useState } from 'react';
import { Send } from 'lucide-react';

export const ChatInput = ({ onSendMessage, disabled = false }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white">
      <div className="max-w-4xl mx-auto p-4">
        <form onSubmit={handleSubmit} className="relative">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Send a message..."
            disabled={disabled}
            className="w-full resize-none rounded-lg border border-gray-300 bg-white px-4 py-3 pr-12 text-gray-900 placeholder-gray-500 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-200 disabled:opacity-50"
            rows={1}
            style={{
              minHeight: '52px',
              maxHeight: '200px',
              overflowY: 'auto',
            }}
          />
          <button
            type="submit"
            disabled={!message.trim() || disabled}
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg bg-green-600 p-2 text-white hover:bg-green-700 disabled:opacity-50 disabled:hover:bg-green-600 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <div className="mt-2 text-xs text-gray-500 text-center">
          Press Enter to send, Shift + Enter for new line
        </div>
      </div>
    </div>
  );
};