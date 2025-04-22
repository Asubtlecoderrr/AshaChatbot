import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom"; // <-- added Link
import "../styles/style.css";

export default function Signup() {
<<<<<<< Updated upstream
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate(); // <-- create navigate instance
=======
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const navigate = useNavigate();

>>>>>>> Stashed changes
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
<<<<<<< Updated upstream
      // Change the URL to point to Flask backend (localhost:5000)
      const res = await fetch("http://localhost:8000/auth/register", {
=======
      const res = await fetch("http://localhost:5000/register", {
>>>>>>> Stashed changes
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (res.status === 201) {
        alert("Signup successful!");
        navigate("/login");
      } else {
        alert(data.message || "Error during signup");
      }
    } catch (err) {
      alert("Error during signup");
    }
  };

<<<<<<< Updated upstream
  return (
    <div className="signup-container">
      {/* Display the welcome message and image */}
      <h1 style={{ color: 'purple', fontWeight: 'bold' }}>Hello, Welcome to Asha AI!</h1>
      {/* Signup section */}
      <p style={{ fontSize: '16px', color: '#555' ,fontWeight: 'bold' }}>Create an account to join Asha AI.</p>

      <form className="form" onSubmit={handleSubmit}>
        <h2>Sign Up</h2>
        <input
          name="name"
          type="text"
          placeholder="Name"
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
=======
return (
  <div className="container">
    <div className="right"> {/* Moved image to left */}
      <img
        src="/images/girl.png"
        alt="Signup visual"
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
>>>>>>> Stashed changes
    </div>
    <div className="left"> {/* Moved form to right */}
      <div className="content">
        <h1>Hello, Welcome to Asha AI !</h1>
        <p>Create an account to join Asha AI.</p>
        <form className="form" onSubmit={handleSubmit}>
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
        <p className="signup-link">
          Already have an account? <Link to="/login">Sign In</Link>
        </p>
      </div>
    </div>
  </div>
);
}
