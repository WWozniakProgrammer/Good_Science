import React from "react";
import "./NavBar.css";

const NavBar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="logo">MatchAI 🐨</div>
        <ul className="nav-links">
          <li>About</li>
          <li>Features</li>
          <li>Contact</li>
          <button className="login-button">Login</button>
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
