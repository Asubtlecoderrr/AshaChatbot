import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom"; // <-- added Link
import "../styles/style.css";

export default function Signup() {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate(); // <-- create navigate instance
  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://104.197.6.224:8000/auth/register", {
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

return (
  <div className="container">
    <div className="right"> {/* Moved image to left */}
      <img
        src="/images/girl.png"
        alt="Signup visual"
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
    </div>
    <div className="left"> {/* Moved form to right */}
      <div className="content">
        <h1>Hello, Welcome to Asha AI !</h1>
        <p>Create an account to join Asha AI.</p>
        <form className="form" onSubmit={handleSubmit}>
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
        <p className="signup-link">
          Already have an account? <Link to="/login">Sign In</Link>
        </p>
      </div>
    </div>
  </div>
);
}
