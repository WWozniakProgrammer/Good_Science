import React, { useState } from "react";
import "./LoginForm.css";

const LoginForm = () => {
  const [preference, setPreference] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form submitted with:", { preference, email, password });
    // Add form submission logic here
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <h2>Find Your Match</h2>
      <div className="form-group">
        <label htmlFor="preference">Preference</label>
        <select
          id="preference"
          value={preference}
          onChange={(e) => setPreference(e.target.value)}
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
      <button type="submit">Submit</button>
    </form>
  );
};

export default LoginForm;
