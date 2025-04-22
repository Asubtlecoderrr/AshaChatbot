import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Layout from "./components/Layout";
import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';

function AppWrapper() {
  const [user, setUser] = useState(null); // null = not logged in
  const [isLogin, setIsLogin] = useState(true); // toggle between login/signup
  const navigate = useNavigate(); // Initialize navigate

  const toggleForm = () => {
    setIsLogin(!isLogin);
    // Navigate to the appropriate page based on the toggle
    navigate(isLogin ? "/signup" : "/login");
  };

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
    <Router> {/* Ensure the entire app is inside the Router */}
      <AppWrapper />
    </Router>
  );
}

export default App;
