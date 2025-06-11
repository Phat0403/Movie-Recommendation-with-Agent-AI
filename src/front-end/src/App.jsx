import { Outlet } from "react-router-dom";
import Header from "./components/Header";
import React, { useState, useEffect } from "react";
import Footer from "./components/Footer";
import MobileNavigation from "./components/MobileNavigation";
import ChatbotFab from "./components/ChatbotFab";
import ChatbotWindow from "./components/ChatbotWindow";
function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };
  return (
    <main className="pb-14 lg:pb-0">
      <Header />
      <div className="">
        <Outlet />
      </div>
      <Footer />

      <>
        <ChatbotFab onClick={toggleChat} />
        <ChatbotWindow
          isOpen={isChatOpen}
          onClose={() => setIsChatOpen(false)}
        />
      </>

      <MobileNavigation />
    </main>
  );
}

export default App;
