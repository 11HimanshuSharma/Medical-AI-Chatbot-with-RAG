import React from 'react';
import { MessageSquare, Plus } from 'lucide-react';

export const Header = ({ onNewChat }) => {
  return (
    <header className="border-b border-gray-200 bg-white sticky top-0 z-10">
      <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <MessageSquare className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-xl font-semibold text-gray-900">MedBot AI</h1>
          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">Medical Assistant</span>
        </div>
        <button
          onClick={onNewChat}
          className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <Plus className="w-4 h-4" />
          New chat
        </button>
      </div>
    </header>
  );
};