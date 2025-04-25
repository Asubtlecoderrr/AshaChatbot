import React, { useRef } from "react";
import Navbar from "./Navbar";
import Chat from "./Chat";
import "../styles/Loader.css";

const Layout = () => {
  const chatRef = useRef();

  const handleBotMessage = (message) => {
    chatRef.current?.addBotMessage(message);
  };


  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <Navbar onBotMessage={handleBotMessage} />
      <div style={{ flex: 1, overflow: 'auto' }}>
        <Chat ref={chatRef} />
      </div>
    </div>
  );
};

export default Layout;
