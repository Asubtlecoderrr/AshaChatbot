// App.js
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Layout from "./components/Layout";
import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';

function AppWrapper() {
  const [user, setUser] = useState(null);
  const [isLogin, setIsLogin] = useState(true);
  const navigate = useNavigate();

  const toggleForm = () => {
    setIsLogin(!isLogin);
    navigate(isLogin ? "/signup" : "/login");
  };

  // Clear session_id on page reload (not on internal navigation)
  useEffect(() => {
    const handleReload = () => {
      localStorage.removeItem("sessionId");
    };

    window.addEventListener("beforeunload", handleReload);
    return () => window.removeEventListener("beforeunload", handleReload);
  }, []);

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route
          path="/login"
          element={user ? <Navigate to="/layout" /> : <Login setUser={setUser} />}
        />
        <Route
          path="/signup"
          element={user ? <Navigate to="/layout" /> : <Signup setUser={setUser} />}
        />
        <Route
          path="/layout"
          element={user ? <Layout /> : <Navigate to="/login" />}
        />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppWrapper />
    </Router>
  );
}

export default App;
