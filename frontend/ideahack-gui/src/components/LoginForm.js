import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./LoginForm.css";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("https://your-endpoint.com/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccessMessage(`Welcome back! User ID: ${data.userId}`);
        setErrorMessage("");
        // Optionally redirect or store user info
      } else {
        throw new Error(data.message || "Failed to login. Please try again.");
      }
    } catch (error) {
      setErrorMessage(error.message);
      setSuccessMessage("");
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <h2>Login to Your Account</h2>
      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <button type="submit">Login</button>
      {errorMessage && <p className="error">{errorMessage}</p>}
      {successMessage && <p className="success">{successMessage}</p>}
      <div className="register-link">
        <p>Don't have an account?</p>
        <Link to="/register">
          <button type="button" className="register-button">
            Register
          </button>
        </Link>
      </div>
    </form>
  );
};

export default LoginForm;
