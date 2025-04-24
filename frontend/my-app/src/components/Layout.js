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
    <div>
      <Navbar onBotMessage={handleBotMessage} />
      <Chat ref={chatRef} />
    </div>
  );
};

export default Layout;
