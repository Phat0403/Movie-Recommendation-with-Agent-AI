// src/components/ConfirmModal.js
import React from 'react';

const ConfirmModal = ({ isOpen, onClose, onConfirm, title, children, isLoading }) => {
  if (!isOpen) return null;

  return (
    // Backdrop
    <div 
      onClick={onClose} 
      className="fixed inset-0 bg-black bg-opacity-50 z-40 flex justify-center items-center"
    >
      {/* Modal content */}
      <div 
        onClick={e => e.stopPropagation()} // Ngăn việc click vào modal làm đóng modal
        className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-4"
      >
        <h3 className="text-xl font-bold text-gray-800 mb-4">{title}</h3>
        <div className="text-gray-600 mb-6">{children}</div>
        <div className="flex justify-end gap-4">
          <button
            onClick={onClose}
            disabled={isLoading}
            className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={isLoading}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50 flex items-center"
          >
            {isLoading && (
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            )}
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmModal;