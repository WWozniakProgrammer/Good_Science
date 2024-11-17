import React from "react";
import { Link } from "react-router-dom";
import "./NavBar.css";

const NavBar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="logo">MatchAI 🐨</div>
        <ul className="nav-links">
          <li>
            <Link to="/about">O Nas</Link>
          </li>
          <li>
            <Link to="/features">Nowości</Link>
          </li>
          <li>
            <Link to="/contact">Kontakt</Link>
          </li>
          <li>
            <Link to="/login">
              <button className="login-button">Zaloguj</button>
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
