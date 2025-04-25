import React, { useState, useEffect, useRef, forwardRef, useImperativeHandle } from "react";
import "../styles/Chat.css";
import Loader from "./Loader";

const Chat = forwardRef((props, ref) => {
  const welcomeMessage = "Hello! Welcome to ASHA AI 💜<br /><br />You're in the perfect place to ask, learn, and grow — because YOU build tomorrow.<br />And it all starts with just one question !!";
  const [userMessage, setUserMessage] = useState("");
  const [messages, setMessages] = useState([{ message: welcomeMessage, className: "bot-message" }]);
  const [isSending, setIsSending] = useState(false);
  const chatContainerRef = useRef(null);
  const token = localStorage.getItem("token");

  useImperativeHandle(ref, () => ({
    addBotMessage: (message) => {
      if (message === "__LOADING__") {
      setIsSending(true);
    } else if (message === "__DONE__") {
      setIsSending(false);
    } else {
      displayMessage(message, "bot-message");
    }
    }
  }));

  const sendMessage = async () => {
    const userMessageText = userMessage.trim();
    if (!userMessageText) return;

    displayMessage(userMessageText, "user-message");
    setUserMessage("");
    setIsSending(true);

    try {
      const response = await fetch('http://104.197.6.224:8000/api/run-flow', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ user_query: userMessageText }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch');
      }

      const data = await response.json();
      const botResponse = data.result?.replace(/\n/g, "<br>") || "Sorry, I didn't understand that.";
      displayMessage(botResponse, "bot-message");
    } catch (error) {
      console.error("Error:", error);
      displayMessage("Something went wrong. Please try again later.", "bot-message");
    } finally {
      setIsSending(false);
    }
  };

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  useEffect(() => {
      scrollToBottom();
  }, [messages.length]);

  const formatMessage = (message, className) => {
    if (className === "user-message") {
      let formatted = message.replace(/\*\*(.*?)\*\*/g, '<strong style="color: white;">$1</strong>');
      const urlRegex = /((https?:\/\/[^\s<]+[^<.,:;"')\]\s]))/g;
      formatted = formatted.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer" style="color: white; text-decoration: underline;">$1</a>');
      return `<span style="color: white;">${formatted}</span>`;
    } else {
      let formatted = message.replace(/\*\*(.*?)\*\*/g, '<strong style="color: black;">$1</strong>');
      const urlRegex = /((https?:\/\/[^\s<]+[^<.,:;"')\]\s]))/g;
      formatted = formatted.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer" style="color: black; text-decoration: underline;">$1</a>');
      return `<span style="color: black;">${formatted}</span>`;
    }
  };

  const displayMessage = (message, className) => {
    const formattedMessage = formatMessage(message, className);
    setMessages((prevMessages) => [...prevMessages, { message: formattedMessage, className, rating: 0 }]);
  };

  return (
    <div className="chat-container">
      <div ref={chatContainerRef} className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.className} ${index}`}>
            <p dangerouslySetInnerHTML={{ __html: message.message }} />
          </div>
        ))}
        {isSending && <Loader />}
      </div>
      <div className="chat-input">
        <form onSubmit={(e) => { e.preventDefault(); sendMessage(); }}>
          <input
            type="text"
            id="user-input"
            placeholder="Type your message..."
            value={userMessage}
            readOnly={isSending}
            onChange={(e) => setUserMessage(e.target.value)}
          />
          <button id="send-button" type="submit" style={{ marginLeft: '7px' }}>
            ASK
          </button>
        </form>
      </div>
    </div>
  );
});

export default Chat;
