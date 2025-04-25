import React, { useState, useRef } from 'react';
import styles from "../styles/Navbar.module.css";
import UploadModal from './UploadModal'; // Import the modal

const Navbar = () => {
  const [uploading, setUploading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const fileInputRef = useRef();
  const token = localStorage.getItem("token");
  console.log(token);
  const uploadDocument = (event) => {
    event.preventDefault();
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    setUploading(true);
    const file = event.target.files[0];

    if (file && file.type === "application/pdf") {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("http://localhost:8000/api/upload-resume/", {
          method: "POST",
          headers: {'Authorization': `Bearer ${token}`, },
          body: formData,
        });

        if (response.ok) {
          sessionStorage.setItem('fileName', file.name);
          setModalVisible(true); // Show success modal
        } else {
          console.error("Upload failed", response.statusText);
          alert("Failed to upload. Try again.");
        }
      } catch (err) {
        console.error("Error uploading file", err);
        alert("Something went wrong!");
      } finally {
        setUploading(false);
      }
    } else {
      alert("Please select a valid PDF file!");
      setUploading(false);
    }
  };

  return (
    <div>
      <nav className={styles.navbar}>
        <div className={styles.leftContent}>
          <img className={styles.logo} src="/images/sap.png" alt="Logo" />
          <div className={styles.ashaTagline}>
            <span className={styles.ashaSlogan}>
              A one-stop assistant for women seeking career advice, resume reviews, and self-improvement tips.
              <br />
              Discover communities, interview questions, courses, and guidance — all in one place.
            </span>
          </div>
        </div>
        <div className={styles.rightContent}>
          <div className={styles.fileUpload}>
            <input
              type="file"
              accept=".pdf"
              className={styles.fileInput}
              ref={fileInputRef}
              onChange={handleFileChange}
              style={{ display: 'none' }} // hide it properly
            />
            <button
              className={`${styles.uploadBtn} ${uploading ? styles.uploadingBtn : ''}`}
              onClick={uploadDocument}
              disabled={uploading}
            >
              {uploading ? 'Uploading...' : 'Upload'}
            </button>
          </div>
        </div>
      </nav>

      <UploadModal
        visible={modalVisible}
        onCancel={() => setModalVisible(false)}
      />
    </div>
  );
};

export default Navbar;
