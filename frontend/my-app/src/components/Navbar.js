import React, { useState, useRef } from 'react';
import styles from "../styles/Navbar.module.css";
import { Alert } from 'react-bootstrap';

const Navbar = ({ onBotMessage }) => {
  const [uploading, setUploading] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const fileInputRef = useRef();
  const token = localStorage.getItem("token");

  const uploadDocument = async (event) => {
    event.preventDefault();
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    setUploading(true);
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
      const formData = new FormData();
      formData.append("file", file);
      onBotMessage?.("✅ Your resume has been uploaded successfully and is being analyzed!");
      onBotMessage?.("__LOADING__");


      try {
        const response = await fetch("http://104.197.6.224:8000/api/upload-resume/", {
          method: "POST",
          headers: { 'Authorization': `Bearer ${token}` },
          body: formData,
        });

        if (response.ok) {
          sessionStorage.setItem('fileName', file.name);
          setShowAlert(true);
          const data = await response.json();
          console.log(data);
          const botResponse = data.result?.replace(/\n/g, "<br>") || "Sorry, I didn't understand that.";
          onBotMessage?.("__DONE__");
          onBotMessage?.(botResponse);
          setTimeout(() => setShowAlert(false), 3000);
        } else {
          alert("Upload failed. Please try again.");
        }
      } catch (err) {
        console.error("Upload error:", err);
        alert("Something went wrong during upload.");
      } finally {
        setUploading(false);
      }
    } else {
      alert("Please select a valid PDF file!");
      setUploading(false);
    }
    fileInputRef.current.value = null;
  };

  return (
    <div>
      <nav className={styles.navbar}>
        <div className={styles.leftContent}>
          <img className={styles.logo} src="/images/sap.png" alt="Logo" />
          <div className={styles.ashaTagline}>
            <span className={styles.ashaBold}></span>
            <span className={styles.ashaSlogan}>
              A one-stop assistant for women seeking career advice, resume reviews, and self-improvement tips. <br />
              Discover communities, interview questions , courses, and guidance — all in one place.
            </span>
          </div>
        </div>
        <div className={styles.rightContent}>
          <div className={styles.fileUpload}>
            <input type="file" accept=".pdf" className={styles.fileInput} ref={fileInputRef} onChange={handleFileChange} />
            <button className={`${styles.uploadBtn} ${uploading ? styles.uploadingBtn : ''}`} onClick={uploadDocument}>
              {uploading ? 'Uploading...' : 'Upload'}
            </button>
          </div>
          {showAlert && (
            <Alert
              variant="success"
              style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                margin: '16px',
                transform: 'translate(-50%, -50%)',
                zIndex: 999,
                backgroundColor: '#6A0DAD',
                color: 'white'
              }}
            >
              Resume Analysis Completed!
            </Alert>
          )}
        </div>
      </nav>
    </div>
  );
};

export default Navbar;
