import React, { useState, useEffect, useRef } from "react";
import "../styles/Chat.css";
import Loader from "./Loader";
import { Spin } from 'antd';
import StarRatings from 'react-star-ratings';

const saveRating = async (message, rating) => {
  console.log('Rating:', rating);
  const url = 'https://gpt-test.lab-us.gcpint.ariba.com:7070/v1/rating'; // replace with your url

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        msg: message,
        vote: rating,
      }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const jsonResponse = await response.json();
    console.log('Rating saved:', jsonResponse);
  } catch (error) {
    console.error('Error:', error);
  }
};

const Chat = () => {
  const welcomeMessage = "Hello! Welcome to ASHA AI 💜<br /><br />You're in the perfect place to ask, learn, and grow — because YOU build tomorrow.<br />And it all starts with just one question !!";
  const [userMessage, setUserMessage] = useState("");
  const [messages, setMessages] = useState([{ message: welcomeMessage, className: "bot-message" }]);
  const [isSending, setIsSending] = useState(false);
  const chatContainerRef = useRef(null);
//  const [isRecording, setIsRecording] = useState(false);
//  const mediaRecorder = useRef(null);
//  const audioChunks = useRef([]);
  const [isFetching, setIsFetching] = useState(false);

//  const handleRecording = async () => {
//    if (isRecording) {
//      if (mediaRecorder.current) {
//        mediaRecorder.current.stop();
//        setIsRecording(false);
//      }
//    } else {
//      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//      mediaRecorder.current = new MediaRecorder(stream);
//
//      mediaRecorder.current.start();
//
//      audioChunks.current = [];
//
//      setIsRecording(true);
//
//      mediaRecorder.current.addEventListener("dataavailable", (event) => {
//        audioChunks.current.push(event.data);
//      });
//
//      mediaRecorder.current.addEventListener("stop", () => {
//        const audioBlob = new Blob(audioChunks.current);
//        const audioUrl = URL.createObjectURL(audioBlob);
//        const formData = new FormData();
//        formData.append('file', audioBlob, 'audio.mp3');
//        console.log(formData)
//        //calling the backend API using fetch
//        setIsFetching(true);
//        fetch('https://gpt-test.lab-us.gcpint.ariba.com:8443/ssr', {
//          method: 'POST',
//          body: formData
//        })
//          .then(response => response.json())
//          .then(data => {
//            setIsFetching(false);
//            setUserMessage(data.text)
//            console.log(data);
//            //you can use the response here
//          })
//          .catch(error => {
//            setIsFetching(false);
//            console.error(error);
//          });
//
//      });
//    }
//  };
  const removeBase64Content = (message) => {
    // Regular expression to match base64 content
    const base64Regex = /data:image\/[a-z]+;base64,([A-Za-z0-9+/]+={0,2})/g;
    // Remove base64 content from the message
    return message.replace(base64Regex, '');
  };
  
  const sendMessage = async () => {
    const userMessageText = userMessage.trim();
    if (userMessageText !== "") {
      displayMessage(userMessageText, "user-message");
      setUserMessage("");
      setIsSending(true);

      const fileName = sessionStorage.getItem('fileName') || '';
      console.log(fileName);

      try {
        let url;
        // Check if fileName is an empty string
        if (fileName === "") {
          url = `http://localhost:8000/v1/ask`;
        } else {
          url = `http://localhost:8000/v1/self-ask?file_name=${encodeURIComponent(fileName.replace(/\s/g, "+"))}&query=${userMessageText}`;
        }

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "messages": [
              ...messages.slice(1).map(msg => ({ "role": msg.className === "user-message" ? "user" : "bot", "message": removeBase64Content(msg.message) })),
              { "role": "user", "message": userMessageText }
            ]
          }),
        });  

        if (response.ok) {
          const data = await response.json();
          // console.log(data);
          const botResponse = data["result"].replace(/\n/g, "<br>");
          const imageBase64 = data["image"];
          if (imageBase64) {
            const imgTag = `<br/><br/><img src="data:image/png;base64,${imageBase64}"  style="width:450px; height:400px" />`;
            displayMessage(botResponse + imgTag, "bot-message");
          } else {
            displayMessage(botResponse, "bot-message");
          }
        } else {
          console.error("Failed to fetch data.");
        }
      } catch (error) {
        console.error("An error occurred:", error);
      } finally {
        setIsSending(false);
      }
    }
  };

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    sessionStorage.removeItem('fileName');
  }, []);

  useEffect(() => {

    setTimeout(() => {
      scrollToBottom();
    }, 100);
  }, [isSending, messages.length]);


  const setRatingForMessage = (messageIndex, newRating) => {
    setMessages((prevMessages) => {
      const newMessages = [...prevMessages];
      newMessages[messageIndex].rating = newRating;
      return newMessages;
    });
    saveRating(messages[messageIndex - 1].message, newRating);
  };

  const displayMessage = (message, className) => {
    setMessages((prevMessages) => [...prevMessages, { message, className, rating: 0 }]);
  };

  return (
    <div className="chat-container">
      <div ref={chatContainerRef} className="chat-messages">

        {messages.map((message, index) => (
          <div key={index} className={`message ${message.className} ${index}`}>
            <p dangerouslySetInnerHTML={{ __html: message.message }} />
            {message.className === 'bot-message' && index !== 0 && (
              <div>
                {message.rating === 0 && (
                  <>
                    <button onClick={() => setRatingForMessage(index, 1)}>👍</button>
                    <button onClick={() => setRatingForMessage(index, -1)}>👎</button>
                  </>
                )}
                {message.rating !== 0 && (
                  <p>Thank you for your feedback!</p>
                )}
              </div>
            )}
          </div>
        ))}
        {isSending && <Loader />}
      </div>
      <div className="chat-input">
        <form onSubmit={(e) => { e.preventDefault(); sendMessage(); }}>
          <Spin spinning={isFetching} size="large" />
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
};

export default Chat;
