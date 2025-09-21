import React from "react";
import "../theme.css";

export default function About() {
  return (
    <div className="container py-5">
      <h2 className="neon-text text-center mb-4">About Us</h2>
      <p className="lead text-center">
        StressDetect is designed to identify early signs of stress among professionals
        using multi-modal data sources including facial, vocal, EEG, and GSR indicators.
      </p>
      <p className="text-center">
        Our mission is to promote workplace wellness, prevent burnout, and enable proactive
        stress management in fast-paced environments.
      </p>
    </div>
  );
}
