import React, { useState } from "react";
import "./Register.css";

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    preference: "",
  });

  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("https://your-endpoint.com/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccessMessage(`Registration successful! User ID: ${data.userId}`);
        setErrorMessage("");
        setFormData({ username: "", email: "", password: "", preference: "" });
      } else {
        throw new Error(
          data.message || "Registration failed. Please try again."
        );
      }
    } catch (error) {
      setErrorMessage(error.message);
      setSuccessMessage("");
    }
  };

  return (
    <form className="register-form" onSubmit={handleSubmit}>
      <h2>Create Your Account</h2>
      <div className="form-group">
        <label htmlFor="username">Username</label>
        <input
          type="text"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="preference">Preference</label>
        <select
          id="preference"
          name="preference"
          value={formData.preference}
          onChange={handleChange}
          required
        >
          <option value="" disabled>
            Select
          </option>
          <option value="investor">Investor</option>
          <option value="academy">Academy</option>
          <option value="business">Business</option>
        </select>
      </div>
      <button type="submit">Register</button>
      {errorMessage && <p className="error">{errorMessage}</p>}
      {successMessage && <p className="success">{successMessage}</p>}
    </form>
  );
};

export default Register;
