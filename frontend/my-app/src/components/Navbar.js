import React, { useState, useRef } from 'react';
import styles from "../styles/Navbar.module.css";
import { Alert } from 'react-bootstrap'; // import Alert from Bootstrap

const Navbar = () => {
  const [uploading, setUploading] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const fileInputRef = useRef();

  const uploadDocument = async (event) => {
    event.preventDefault();
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    setUploading(true);  // set the uploading state as started
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/upload-file/", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        sessionStorage.setItem('fileName', file.name);
        setUploading(false); // set the uploading state as finished
        setShowAlert(true); // show the alert
        setTimeout(() => setShowAlert(false), 3000); // close the alert after 4 seconds
      }
    } else {
      alert("Please select a valid PDF file!");
      setUploading(false);  // set the uploading state as finished
    }
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
                backgroundColor: '#006BB8',
                color: 'white'
              }}
            >
              Your file has been uploaded successfully!
            </Alert>
          )}
        </div>
      </nav>
    </div>
  );
};

export default Navbar;
