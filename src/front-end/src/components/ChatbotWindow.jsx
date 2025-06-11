import React, { useState, useEffect, useRef } from 'react';
import { initConversation, postMessage } from '../hooks/useChatbot'; // Adjust the import path as necessary
import { useNavigate } from 'react-router-dom';

const CloseIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
  </svg>
);

const PaperAirplaneIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
  </svg>
);
export const FilmIcon= (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M6 20.25h12m-7.5-3.75v3.75m3.75-3.75v3.75m-7.5-3.75L3 16.5m18 0-3.75 3.75M3 16.5V6a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 6v10.5m-18 0v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-12 0h3.75" />
  </svg>
);

export const ChatBubbleOvalLeftEllipsisIcon = (props) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" {...props}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M18 10.5H18M15 10.5H15M12 10.5H12M7.5 21V12.75A5.25 5.25 0 0 1 12.75 7.5h4.5A5.25 5.25 0 0 1 22.5 12.75V21M7.5 21H5.25A2.25 2.25 0 0 1 3 18.75V10.5A2.25 2.25 0 0 1 5.25 8.25H7.5" />
  </svg>
);
const ChatbotWindow = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [isInitializing, setIsInitializing] = useState(false);
  const [chatError, setChatError] = useState(null);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);
useEffect(() => {
    if (isOpen) {
      if (!conversationId && !isInitializing) {
        setIsInitializing(true);
        setChatError(null);
        initConversation()
          .then((data) => {
            setConversationId(data.conversation_id);
            // If your initConversation API returns an initial message, you can add it here:
            // if (data.messages) {
            //   setMessages([{ id: 'init-bot', text: data.messages, sender: 'bot', timestamp: new Date() }]);
            // }
            inputRef.current?.focus();
          })
          .catch((err) => {
            console.error("Chat initialization error:", err);
            setChatError(err.message || "Failed to initialize chat. Please try again later.");
          })
          .finally(() => {
            setIsInitializing(false);
          });
      } else if (conversationId) {
        inputRef.current?.focus();
        setChatError(null); // Clear previous errors if conversation is now active
      }
    }
  }, [isOpen, conversationId, isInitializing]);


  const handleSendMessage = async () => {
    if (inputValue.trim() === '' || isSending || !conversationId || isInitializing) return;

    const userMessage = {
      id: `user-${Date.now()}`,
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    const currentInputValue = inputValue;
    setInputValue('');
    setIsSending(true);
    setChatError(null);

    const botMessageId = `bot-${Date.now()}`;
    setMessages((prevMessages) => [
      ...prevMessages,
      { id: botMessageId, text: '', sender: 'bot', timestamp: new Date(), isLoading: true },
    ]);

    try {
      const response = await postMessage(conversationId, currentInputValue);
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === botMessageId 
            ? { ...msg, text: response.messages, isLoading: false, conversation_id: response.conversation_id } 
            : msg
        )
      );
      console.log("Response from bot:", response);
      if (response.intent === 'search by description'){
        navigate('/recommendations', {
          state: { data: response.tconsts }});
      }
      else if (response.intent === 'search by movie name') {
        navigate('/recommendations', {
          state: { data: response.tconsts }});
      }
      // Optional: update conversationId if it can change per message, though unlikely for this API structure
      // setConversationId(response.conversation_id); 
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.id === botMessageId
            ? { ...msg, text: 'Oops! Something went wrong.', isLoading: false, isError: true, errorMessage: error.message || "Failed to get response." }
            : msg
        )
      );
    } finally {
      setIsSending(false);
      inputRef.current?.focus();
    }
  };
  
  if (!isOpen) return null;

  let placeholderText = "Ask about movies...";
  if (isInitializing) {
    placeholderText = "Initializing chat...";
  } else if (!conversationId && chatError) {
    placeholderText = "Chat initialization failed.";
  } else if (!conversationId) {
    placeholderText = "Connecting to chat..."; // General state before init or if init is slow
  }
  return (
    <div 
      className="fixed bottom-6 right-6 md:bottom-20 md:right-6 w-[calc(100%-3rem)] sm:w-full max-w-sm md:max-w-md h-[calc(100vh-8rem)] sm:h-[70vh] max-h-[500px] md:max-h-[600px] bg-neutral-800 shadow-2xl rounded-xl flex flex-col transform transition-all duration-300 ease-in-out animate-slide-up z-[100]"
      role="dialog"
      aria-modal="true"
      aria-labelledby="chatbot-title"
    >
      <header className="bg-neutral-700 p-3 flex justify-between items-center rounded-t-xl border-b border-neutral-600 flex-shrink-0">
        <div className="flex items-center">
          <FilmIcon className="w-5 h-5 text-sky-400 mr-2" aria-hidden="true" />
          <h3 id="chatbot-title" className="text-md font-semibold text-gray-100">CineSuggest AI</h3>
        </div>
        <button 
          onClick={onClose} 
          className="text-gray-400 hover:text-white p-1 rounded-full hover:bg-neutral-600 transition-colors" 
          aria-label="Close chat"
        >
          <CloseIcon className="w-5 h-5" />
        </button>
      </header>

      <div className="flex-grow p-3 space-y-3 overflow-y-auto no-scrollbar bg-neutral-800">
        {chatError && !isInitializing && !conversationId && (
          <div className="bg-red-700/50 border border-red-600 text-red-200 p-2.5 rounded-lg text-xs text-center mb-2 mx-1" role="alert">
            {chatError}
          </div>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] p-2.5 rounded-xl shadow-md text-sm ${
                msg.sender === 'user'
                  ? 'bg-sky-600 text-white rounded-br-none'
                  : `text-gray-100 rounded-bl-none ${msg.isError ? 'bg-red-600 border border-red-500' : 'bg-neutral-600'}`
              }`}
            >
              <p className="whitespace-pre-wrap break-words">
                {msg.isLoading && !msg.text ? (
                  <div className="flex items-center space-x-1.5 py-1">
                    <span className="typing-dot"></span>
                    <span className="typing-dot animation-delay-200"></span>
                    <span className="typing-dot animation-delay-400"></span>
                  </div>
                ) : msg.text}
                {msg.isError && msg.errorMessage && <span className="block text-xs mt-1 text-red-100 opacity-90">{msg.errorMessage}</span>}
              </p>
              <p className={`text-xs mt-1.5 opacity-70 ${msg.sender === 'user' ? 'text-sky-200 text-right' : 'text-gray-400 text-left'}`}>
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <footer className="p-3 border-t border-neutral-600 bg-neutral-700 rounded-b-xl flex-shrink-0">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="flex items-center space-x-2"
        >
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={placeholderText}
            className="flex-grow bg-neutral-600 text-gray-100 placeholder-neutral-400 rounded-full py-2.5 px-4 focus:ring-2 focus:ring-sky-500 focus:outline-none disabled:opacity-60 text-sm transition-colors"
            disabled={isSending || !conversationId || isInitializing}
            aria-label="Chat message input"
          />
          <button
            type="submit"
            disabled={isSending || inputValue.trim() === '' || !conversationId || isInitializing}
            className="bg-sky-600 hover:bg-sky-500 text-white p-2.5 rounded-full focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 focus:ring-offset-neutral-700 disabled:opacity-60 disabled:hover:bg-sky-600 transition-colors"
            aria-label="Send message"
          >
            <PaperAirplaneIcon className="w-5 h-5" />
          </button>
        </form>
      </footer>
      <style>{`
        @keyframes slide-up {
          from { opacity: 0; transform: translateY(20px) scale(0.95); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .animate-slide-up { animation: slide-up 0.3s ease-out forwards; }

        .typing-dot {
          display: inline-block;
          width: 7px;
          height: 7px;
          background-color: currentColor;
          border-radius: 50%;
          opacity: 0.4;
          animation: typing-blink 1.4s infinite both;
        }
        .typing-dot.animation-delay-200 {
          animation-delay: 0.2s;
        }
        .typing-dot.animation-delay-400 {
          animation-delay: 0.4s;
        }
        @keyframes typing-blink {
          0% { opacity: 0.4; transform: scale(0.8); }
          20% { opacity: 1; transform: scale(1); }
          100% { opacity: 0.4; transform: scale(0.8); }
        }
      `}</style>
    </div>
  )
}

export default ChatbotWindow