import React from 'react';
import { MessageSquare, FileText, Stethoscope, Pill, Activity } from 'lucide-react';

export const EmptyState = ({ onExampleClick }) => {
  const examples = [
    {
      icon: Stethoscope,
      text: "What are the symptoms of hypertension?",
      color: "text-red-600",
      bg: "bg-red-50"
    },
    {
      icon: Pill,
      text: "Drug interactions with Warfarin",
      color: "text-blue-600",
      bg: "bg-blue-50"
    },
    {
      icon: Activity,
      text: "Interpret lab values: High WBC count",
      color: "text-green-600",
      bg: "bg-green-50"
    },
    {
      icon: FileText,
      text: "Latest guidelines for diabetes management",
      color: "text-purple-600",
      bg: "bg-purple-50"
    }
  ];

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
      <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6">
        <MessageSquare className="w-8 h-8 text-white" />
      </div>
      
      <h2 className="text-2xl font-semibold text-gray-900 mb-2">
        How can I assist you medically today?
      </h2>
      
      <p className="text-gray-600 mb-8 max-w-md">
        I'm your AI medical assistant. Ask questions about treatments, drug interactions, lab results, or medical guidelines. I'll provide evidence-based answers from trusted medical sources.
      </p>

      <div className="grid gap-3 w-full max-w-md">
        {examples.map((example, index) => (
          <button
            key={index}
            onClick={() => onExampleClick(example.text)}
            className={`flex items-center gap-3 p-4 rounded-xl border border-gray-200 hover:border-gray-300 transition-all hover:shadow-sm text-left ${example.bg}`}
          >
            <example.icon className={`w-5 h-5 ${example.color} flex-shrink-0`} />
            <span className="text-gray-800 text-sm">{example.text}</span>
          </button>
        ))}
      </div>
    </div>
  );
};