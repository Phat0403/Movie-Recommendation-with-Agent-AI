import React from 'react'
import PlusIcon from './icons/PlusIcon'
export const ChatBubbleOvalLeftEllipsisIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M18 10.5H18M15 10.5H15M12 10.5H12M7.5 21V12.75A5.25 5.25 0 0 1 12.75 7.5h4.5A5.25 5.25 0 0 1 22.5 12.75V21M7.5 21H5.25A2.25 2.25 0 0 1 3 18.75V10.5A2.25 2.25 0 0 1 5.25 8.25H7.5" />
  </svg>
);
const ChatbotFab = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="fixed bottom-16 right-6 md:bottom-12 md:right-4 bg-sky-600 hover:bg-sky-700 text-white p-4 rounded-full shadow-xl focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-opacity-50 transition-all duration-300 ease-in-out transform hover:scale-110 z-100 cursor-pointer"
      aria-label="Open chat"
    >
      <ChatBubbleOvalLeftEllipsisIcon className="w-6 h-6" />
    </button>
  );
}

export default ChatbotFab