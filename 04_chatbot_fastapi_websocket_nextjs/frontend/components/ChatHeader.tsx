import React from 'react';

interface ChatHeaderProps {
  connected: boolean;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ connected }) => {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm p-4 border-b border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="text-xl font-semibold text-gray-800 dark:text-white">Chatbot</div>
          <div className="flex items-center">
            <div className={`w-2 h-2 rounded-full mr-2 ${connected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-600 dark:text-gray-300">
              {connected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
        <div>
          <button className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-md text-gray-600 dark:text-gray-300 transition">
            Clear Chat
          </button>
        </div>
      </div>
    </header>
  );
};

export default ChatHeader; 