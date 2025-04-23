import React from "react";
import "../styles/Loader.css"; // Import the CSS file

const Loader = () => {
  return (
    <div className="loader-wrapper">
      <span className="thinking-text">Thinking</span>
      <div className="dot-loader">
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  );
};

export default Loader;
