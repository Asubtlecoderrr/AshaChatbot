import React, { useEffect, useState } from "react";
import "../styles/SessionList.css";

/**
 * Props:
 *  - onSelectSession(sessionId: string | null)
 *  - refreshKey: number        // <-- New prop from Layout
 */
const SessionList = ({ onSelectSession, refreshKey }) => {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSessions = async () => {
      setLoading(true);
      try {
        const res = await fetch("http://localhost:8000/api/sessions", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!res.ok) throw new Error("Failed to load sessions");
        const data = await res.json();
        setSessions(data || []);
      } catch (err) {
        console.error("Failed to fetch sessions:", err);
        setSessions([]);
      } finally {
        setLoading(false);
      }
    };
    fetchSessions();
  }, [refreshKey]);  // <— re-run fetch when this changes

  const handleClick = (sessionId) => {
    setSelectedSession(sessionId);
    localStorage.setItem("sessionId", sessionId);
    onSelectSession?.(sessionId);
  };

  const handleNewChat = () => {
    setSelectedSession(null);
    localStorage.removeItem("sessionId");
    onSelectSession?.(null);
  };

  return (
    <div className="session-list-container">
      <div className="session-list-header">
        <div className="session-list-title">Your Sessions</div>
        <button className="new-chat-btn" onClick={handleNewChat}>
          +
        </button>
      </div>
      {loading ? (
        <div>Loading sessions...</div>
      ) : (
        sessions.map((sessionId) => (
          <div
            key={sessionId}
            className={`session-item ${
              selectedSession === sessionId ? "selected" : ""
            }`}
            onClick={() => handleClick(sessionId)}
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleClick(sessionId);
            }}
          >
            {sessionId}
          </div>
        ))
      )}
    </div>
  );
};

export default SessionList;
