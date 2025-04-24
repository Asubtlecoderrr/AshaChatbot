import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
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
      const res = await fetch("http://104.197.6.224:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (res.status === 200) {
        alert("Login successful!");
        localStorage.setItem("token", data.access_token); //dont remove thissssss 
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
<div className="container">
  <div className="left">
    <div className="content">
      <h1 className="left-text">Welcome Back to ASHA AI</h1>
      <p className="left-text">Please sign in to continue</p>
      <form onSubmit={handleSubmit} className="form">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Sign In</button>
      </form>
      <p className="signup-link left-text">
        Don’t have an account? <a href="/signup">Sign Up</a>
      </p>
    </div>
  </div>
  <div className="right">
    <img
      src="/images/girl.png"
      alt="Login visual"
      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
    />
  </div>
</div>

  );
}
