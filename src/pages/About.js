import React from "react";
import "../theme.css";

export default function About() {
  return (
    <div className="container py-5">
      <div className="text-center mb-5">
        <h2 className="neon-text">About StressConnect</h2>
        <p className="lead">
          Advancing personal wellbeing through intelligent stress detection technology
        </p>
      </div>

      <div className="row mb-5">
        <div className="col-md-6">
          <div className="neon-card fade-in-up">
            <h3>Our Mission</h3>
            <p>
              StressConnect is dedicated to helping people build healthier daily routines by providing
              real-time stress detection and monitoring solutions. We believe that early 
              intervention is key to preventing burnout and maintaining optimal mental health 
              in everyday life.
            </p>
            <p>
              Our cutting-edge technology combines multiple biometric indicators to deliver 
              accurate, non-invasive stress assessment tools that empower individuals and communities
              to take proactive steps in wellbeing.
            </p>
          </div>
        </div>
        <div className="col-md-6">
          <div className="neon-card slide-in-right">
            <h3>Our Vision</h3>
            <p>
              We envision a future where stress is detected and addressed before
              it becomes a critical issue. Through our innovative platform, we aim to create 
              a world where everyone has access to personalized stress management
              insights and support.
            </p>
            <p>
              By leveraging artificial intelligence and advanced biometric analysis, we're 
              building the foundation for more empathetic, responsive, and productive 
              everyday environments.
            </p>
          </div>
        </div>
      </div>

      <div className="row mb-5">
        <div className="col-12">
          <div className="neon-card">
            <h3 className="text-center mb-4">How It Works</h3>
            <div className="row">
              <div className="col-md-6">
                <h4>Multi-Modal Detection</h4>
                <p>
                  Our platform utilizes four key biometric indicators to provide comprehensive 
                  stress analysis:
                </p>
                <ul className="list-unstyled">
                  <li>📸 Facial Expression Analysis</li>
                  <li>🎤 Voice Pattern Recognition</li>
                  <li>🧠 EEG Brain Activity Monitoring</li>
                  <li>⚡ GSR Physiological Response Tracking</li>
                </ul>
              </div>
              <div className="col-md-6">
                <h4>Real-Time Insights</h4>
                <p>
                  Advanced machine learning algorithms process your biometric data to deliver 
                  instant stress level assessments and personalized recommendations. Our system 
                  continuously learns and adapts to provide increasingly accurate insights over time.
                </p>
                <p>
                  All data is processed with the highest security standards, ensuring your 
                  privacy while delivering actionable wellness insights.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-md-4">
          <div className="neon-card text-center">
            <h4>Privacy First</h4>
            <p>
              Your biometric data is encrypted and processed locally whenever possible. 
              We maintain strict data protection protocols and never share personal 
              information without explicit consent.
            </p>
          </div>
        </div>
        <div className="col-md-4">
          <div className="neon-card text-center">
            <h4>Scientifically Backed</h4>
            <p>
              Our algorithms are based on peer-reviewed research in psychology, 
              neuroscience, and stress science. We collaborate with leading
              institutions to ensure accuracy and effectiveness.
            </p>
          </div>
        </div>
        <div className="col-md-4">
          <div className="neon-card text-center">
            <h4>Easy Integration</h4>
            <p>
              Designed for seamless integration into existing wellbeing
              programs. Our platform works with standard devices and requires 
              minimal setup for maximum impact.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}