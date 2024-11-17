import React from "react";
import { Link } from "react-router-dom";
import "./NavBar.css";

const NavBar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="logo">
          <Link to="/">
            <button className="logo-button">MatchAI 🐨</button>
          </Link>
        </div>
        <ul className="nav-links">
          <li>
            <Link to="/about">
              <button className="login-button">About</button>
            </Link>
          </li>
          <li>
            <Link to="/features">
              <button className="login-button">Features</button>
            </Link>
          </li>
          <li>
            <Link to="/contact">
              <button className="login-button">Contact</button>
            </Link>
          </li>
          <li>
            <Link to="/login">
              <button className="login-button">Login</button>
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
