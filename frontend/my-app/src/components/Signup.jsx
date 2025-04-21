import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // <-- import navigate hook
import "../styles/style.css"; // Adjust the path if needed

export default function Signup() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const navigate = useNavigate(); // <-- create navigate instance
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Change the URL to point to Flask backend (localhost:5000)
      const res = await fetch("http://localhost:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (res.status === 201) {
        alert("Signup successful!");
        navigate("/login"); // <-- redirect to login
      } else {
        alert(data.message || "Error during signup");
      }
    } catch (err) {
      alert("Error during signup");
    }
  };

  return (
    <div className="signup-container">
      {/* Display the welcome message and image */}
      <h1 style={{ color: 'purple', fontWeight: 'bold' }}>Hello, Welcome to Asha AI!</h1>
      {/* Signup section */}
      <p style={{ fontSize: '16px', color: '#555' ,fontWeight: 'bold' }}>Create an account to join Asha AI.</p>

      <form className="form" onSubmit={handleSubmit}>
        <h2>Sign Up</h2>
        <input
          name="username"
          type="text"
          placeholder="Username"
          onChange={handleChange}
          required
        />
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
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}
