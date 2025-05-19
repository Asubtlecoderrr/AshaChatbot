import React, {
  useState,
  useEffect,
  useRef,
  forwardRef,
  useImperativeHandle,
} from "react";
import "../styles/Chat.css";
import Loader from "./Loader";

const Chat = forwardRef(({ sessionMessages = [], sessionId, onSessionIdReceived }, ref) => {
  const welcomeMessage =
    "Hello! Welcome to ASHA AI 💜<br /><br />You're in the perfect place to ask, learn, and grow — because YOU build tomorrow.<br />And it all starts with just one question !!";
  const [userMessage, setUserMessage] = useState("");
  const [messages, setMessages] = useState([
    { message: welcomeMessage, className: "bot-message" },
  ]);
  const [isSending, setIsSending] = useState(false);
  const chatContainerRef = useRef(null);
  const token = localStorage.getItem("token");

  // Expose addBotMessage to parent via ref
  useImperativeHandle(ref, () => ({
    addBotMessage: (msg) => {
      if (msg === "__LOADING__") {
        setIsSending(true);
      } else if (msg === "__DONE__") {
        setIsSending(false);
      } else {
        displayMessage(msg, "bot-message");
      }
    },
  }));

  useEffect(() => {
    if (sessionMessages.length > 0) {
      const formatted = sessionMessages.map((m) => ({
        message: formatMessage(
          m.text.replace(/\n/g, "<br>"),
          m.sender === "user" ? "user" : "bot-message"
        ),
        className: m.sender === "user" ? "user-message" : "bot-message",
      }));
      setMessages([{ message: welcomeMessage, className: "bot-message" }, ...formatted]);
    }
  }, [sessionMessages, sessionId]);

  useEffect(() => {
    if (!sessionId) {
      setMessages([
        { message: welcomeMessage, className: "bot-message" }
      ]);
    }
  }, [sessionId]);

  const sendMessage = async () => {
    const text = userMessage.trim();
    if (!text) return;

    displayMessage(text, "user-message");
    setUserMessage("");
    setIsSending(true);

    try {
      let res = null;
      if (!sessionId) {
        res = await fetch("http://localhost:8000/api/run-flow", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ user_query: text }),
        });
      } else {
        res = await fetch("http://localhost:8000/api/run-flow", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ user_query: text,  session_id: sessionId }),
        });
      }
      if (!res.ok) throw new Error("Failed to send message");
      const data = await res.json();

      if (data.session_id && data.session_id !== sessionId) {
        // Notify Layout to update sessionId
        onSessionIdReceived(data.session_id);
      }

      const botResp = (data.result || "")
        .replace(/\n/g, "<br>")
        .trim();
      displayMessage(botResp, "bot-message");
    } catch (err) {
      console.error("Error:", err);
      displayMessage(
        "Something went wrong. Please try again later.",
        "bot-message"
      );
    } finally {
      setIsSending(false);
    }
  };

  // Auto-scroll on new message
  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  };
  useEffect(scrollToBottom, [messages.length, isSending]);

  // Formatting & display helpers
  const formatMessage = (msg, cls) => {
    let formatted = msg.replace(/\*\*(.*?)\*\*/g, `<strong>${"$1"}</strong>`);
    const urlRegex = /((https?:\/\/[^\s<]+[^<.,:;"')\]\s]))/g;
    formatted = formatted.replace(
      urlRegex,
      `<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>`
    );
    return `<span>${formatted}</span>`;
  };
  const displayMessage = (msg, cls) => {
    setMessages((prev) => [
      ...prev,
      { message: formatMessage(msg, cls), className: cls },
    ]);
  };

  return (
    <div className="chat-container">
      <div ref={chatContainerRef} className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.className}`}>
            <p dangerouslySetInnerHTML={{ __html: m.message }} />
          </div>
        ))}
        {isSending && <Loader />}
      </div>
      <div className="chat-input">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            sendMessage();
          }}
        >
          <input
            type="text"
            placeholder="Type your message..."
            value={userMessage}
            readOnly={isSending}
            onChange={(e) => setUserMessage(e.target.value)}
          />
          <button type="submit">ASK</button>
        </form>
      </div>
    </div>
  );
});

export default Chat;
