import React from 'react';

const ConnectingOverlay: React.FC = () => {
  return (
    <div className="fixed inset-0 bg-white/90 dark:bg-gray-900/90 z-50 flex flex-col items-center justify-center">
      <div className="w-16 h-16 mb-4 relative">
        <div className="absolute inset-0 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-2">Connecting</h3>
      <p className="text-gray-600 dark:text-gray-300 text-center max-w-md px-4">
        Establishing connection to the chat server...
      </p>
    </div>
  );
};

export default ConnectingOverlay; 