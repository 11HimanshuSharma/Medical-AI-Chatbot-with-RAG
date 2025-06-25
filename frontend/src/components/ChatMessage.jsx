import React from 'react';
import { User, Bot } from 'lucide-react';

export const ChatMessage = ({ message, isUser }) => {
  return (
    <div className={`flex gap-4 p-6 ${isUser ? 'bg-gray-50' : 'bg-white'}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-gray-700' : 'bg-green-600'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>
      <div className="flex-1 space-y-2">
        <div className="text-sm font-medium text-gray-900">
          {isUser ? 'You' : 'ChatGPT'}
        </div>
        <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
          {message}
        </div>
      </div>
    </div>
  );
};