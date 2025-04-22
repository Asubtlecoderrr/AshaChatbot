import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/style.css";

export default function Login({ setUser }) {
  const [form, setForm] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (res.status === 200) {
        alert("Login successful!");
        localStorage.setItem("token", data.access_token);
        setUser(true); 
        navigate("/layout"); 
      } else {
        alert(data.message || "Invalid credentials");
      }
    } catch (err) {
      alert("Error during login");
    }
  };

  return (
  <div className="signup-container">
      {/* Display the welcome message and image */}
      <h1 style={{ color: 'purple', fontWeight: 'bold' }}>Hello , Welcome to Asha AI!</h1>
      {/* Login section */}
      <p style={{ fontSize: '16px', color: '#555' ,fontWeight: 'bold'}}>You are just one step away to experience Asha AI</p>


    <form className="form" onSubmit={handleSubmit}>
      <h2>Login</h2>
      <input
        name="email"
        type="email"
        placeholder="Email"
        onChange={handleChange}
        required
      />
      <input
        name="password"
        type="password"
        placeholder="Password"
        onChange={handleChange}
        required
      />
      <button type="submit">Login</button>
    </form>
      </div>
  );
}
