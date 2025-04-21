import React from "react";
import Navbar from "./Navbar";
import Chat from "./Chat";
import "../styles/Loader.css";

const Layout = () => {
  return (
    <div>
      <Navbar />
      <Chat />
    </div>
  );
};

export default Layout;
