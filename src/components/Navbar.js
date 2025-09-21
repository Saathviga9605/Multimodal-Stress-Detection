import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark neon-border">
      <div className="container">
        <Link className="navbar-brand neon-text fw-bold" to="/">StressDetect</Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto d-flex align-items-center">
            <li className="nav-item">
              <Link className="nav-link neon-link" to="/">Home</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link neon-link" to="/about">About</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link neon-link" to="/features">Features</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link neon-link" to="/impact">Impact</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link btn btn-neon ms-3 px-3" to="/dashboard">Dashboard</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}
