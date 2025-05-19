// Layout.js
import React, { useRef, useState, useEffect } from "react";
import Navbar from "./Navbar";
import Chat from "./Chat";
import SessionList from "./SessionList";
import "../styles/Layout.css";

const Layout = () => {
  const chatRef = useRef();
  const [sessionMessages, setSessionMessages] = useState([]);
  const [sessionId, setSessionId] = useState(
    localStorage.getItem("sessionId") || null
  );
  const [sessionRefreshKey, setSessionRefreshKey] = useState(0);

  useEffect(() => {
    if (sessionId) {
      loadSession(sessionId);
    }
  }, [sessionId]);

  const loadSession = async (id) => {
    try {
      const res = await fetch(
        `http://localhost:8000/api/session/${id}/messages`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      const data = await res.json();
      setSessionMessages(data.messages || []);
      setSessionId(id);
      localStorage.setItem("sessionId", id);
    } catch {
      setSessionMessages([]);
    }
  };

  const handleSelectSession = (id) => {
    if (id) {
      loadSession(id);
    } else {
      setSessionMessages([]);
      setSessionId(null);
      localStorage.removeItem("sessionId");
      setSessionRefreshKey((k) => k + 1);
    }
  };

  const handleBotMessage = (msg) => {
    chatRef.current?.addBotMessage(msg);
  };

  const handleSessionIdReceived = (newSessionId) => {
    setSessionId(newSessionId);
    localStorage.setItem("sessionId", newSessionId);
    setSessionRefreshKey((k) => k + 1);
  };

  return (
    <div className="layout-root">
      <Navbar
        onBotMessage={handleBotMessage}
        onSessionIdReceived={handleSessionIdReceived} // ✅ Add this
      />
      <div className="layout-main">
        <div className="sidebar">
          <SessionList
            onSelectSession={handleSelectSession}
            refreshKey={sessionRefreshKey}
          />
        </div>
        <div className="chat-panel">
          <Chat
            ref={chatRef}
            sessionMessages={sessionMessages}
            sessionId={sessionId}
            onSessionIdReceived={handleSessionIdReceived}
          />
        </div>
      </div>
    </div>
  );
};

export default Layout;
