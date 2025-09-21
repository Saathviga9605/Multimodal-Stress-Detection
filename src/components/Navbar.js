import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import "../theme.css";

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar">
      <div className="container">
        <Link className="navbar-brand" to="/">
          StressConnect
        </Link>

        <button
          className="navbar-toggler"
          onClick={toggleMenu}
          aria-label="Toggle navigation"
        >
          <div className="hamburger">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </button>

        <ul className={`navbar-nav ${isMenuOpen ? 'show' : ''}`}>
          <li className="nav-item">
            <Link 
              className={`nav-link neon-link ${isActive('/') ? 'active' : ''}`} 
              to="/"
              onClick={() => setIsMenuOpen(false)}
            >
              Home
            </Link>
          </li>
          <li className="nav-item">
            <Link 
              className={`nav-link neon-link ${isActive('/about') ? 'active' : ''}`} 
              to="/about"
              onClick={() => setIsMenuOpen(false)}
            >
              About
            </Link>
          </li>
          <li className="nav-item">
            <Link 
              className={`nav-link neon-link ${isActive('/features') ? 'active' : ''}`} 
              to="/features"
              onClick={() => setIsMenuOpen(false)}
            >
              Features
            </Link>
          </li>
          <li className="nav-item">
            <Link 
              className={`nav-link neon-link ${isActive('/impact') ? 'active' : ''}`} 
              to="/impact"
              onClick={() => setIsMenuOpen(false)}
            >
              Impact
            </Link>
          </li>
          <li className="nav-item">
            <Link 
              className="nav-link btn btn-neon ms-3 px-3" 
              to="/dashboard"
              onClick={() => setIsMenuOpen(false)}
            >
              Dashboard
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}