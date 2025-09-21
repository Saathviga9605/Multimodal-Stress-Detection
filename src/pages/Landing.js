import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <section className="hero">
      <motion.div 
        className="container"
        initial={{ opacity: 0, y: -50 }} 
        animate={{ opacity: 1, y: 0 }} 
        transition={{ duration: 1 }}
      >
        <h1 className="neon-text">Intelligent Stress Detection</h1>
        <p className="lead">Real-time insights into workplace mental well-being</p>
        <div>
          <Link to="/dashboard" className="btn btn-neon me-3">Start Detection</Link>
          <Link to="/features" className="btn btn-outline-neon">Learn More</Link>
        </div>
      </motion.div>
    </section>
  );
}
