import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import "../theme.css";

export default function Landing() {
  return (
    <>
      {/* Hero Section */}
      <section className="hero">
        <motion.div 
          className="container text-center"
          initial={{ opacity: 0, y: -50 }} 
          animate={{ opacity: 1, y: 0 }} 
          transition={{ duration: 1 }}
        >
          <h1 className="neon-text">Intelligent Stress Detection</h1>
          <p className="lead">
            Revolutionary multi-modal technology for real-time workplace wellness monitoring 
            and proactive mental health support
          </p>
          <div className="btn-group">
            <Link to="/dashboard" className="btn btn-neon me-3">Start Detection</Link>
            <Link to="/features" className="btn btn-outline-neon">Learn More</Link>
          </div>
        </motion.div>
      </section>

      {/* Key Features Preview */}
      <section className="container py-5">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="neon-text text-center mb-5">Why Choose StressConnect?</h2>
          <div className="row">
            <div className="col-md-4 mb-4">
              <div className="neon-card text-center fade-in-up">
                <div style={{fontSize: '3rem', marginBottom: '1rem'}}>🎯</div>
                <h4>94% Accuracy</h4>
                <p>
                  Advanced AI algorithms trained on thousands of stress patterns 
                  deliver industry-leading detection accuracy.
                </p>
              </div>
            </div>
            <div className="col-md-4 mb-4">
              <div className="neon-card text-center fade-in-up" style={{animationDelay: '0.2s'}}>
                <div style={{fontSize: '3rem', marginBottom: '1rem'}}>⚡</div>
                <h4>Real-Time Analysis</h4>
                <p>
                  Instant stress assessment with live feedback and immediate 
                  recommendations for stress management.
                </p>
              </div>
            </div>
            <div className="col-md-4 mb-4">
              <div className="neon-card text-center fade-in-up" style={{animationDelay: '0.4s'}}>
                <div style={{fontSize: '3rem', marginBottom: '1rem'}}>🔒</div>
                <h4>Privacy First</h4>
                <p>
                  HIPAA-compliant data protection with local processing and 
                  encrypted storage for maximum security.
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Technology Overview */}
      <section style={{background: 'rgba(178, 187, 95, 0.05)', padding: '4rem 0'}}>
        <div className="container">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="neon-text text-center mb-5">Multi-Modal Detection Technology</h2>
            <div className="row align-items-center">
              <div className="col-md-6">
                <div className="neon-card">
                  <h3>Four Integrated Detection Methods</h3>
                  <div style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
                    <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                      <span style={{fontSize: '2rem'}}>📸</span>
                      <div>
                        <strong>Facial Analysis:</strong> Micro-expression and tension detection
                      </div>
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                      <span style={{fontSize: '2rem'}}>🎤</span>
                      <div>
                        <strong>Voice Analysis:</strong> Vocal pattern and frequency assessment
                      </div>
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                      <span style={{fontSize: '2rem'}}>🧠</span>
                      <div>
                        <strong>EEG Monitoring:</strong> Brainwave pattern analysis
                      </div>
                    </div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                      <span style={{fontSize: '2rem'}}>⚡</span>
                      <div>
                        <strong>GSR Tracking:</strong> Physiological response monitoring
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-md-6 text-center">
                <div style={{
                  fontSize: '8rem',
                  background: 'linear-gradient(45deg, #b2bb5f, #8d9740)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  filter: 'drop-shadow(0 4px 8px rgba(178, 187, 95, 0.3))'
                }}>
                  🧬
                </div>
                <h4 style={{color: '#465b26', marginTop: '1rem'}}>
                  Comprehensive Biometric Analysis
                </h4>
                <p>
                  Our integrated approach combines multiple data streams for 
                  unparalleled accuracy in stress detection and assessment.
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="container py-5">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="neon-text text-center mb-5">Transform Your Workplace Wellness</h2>
          <div className="row">
            <div className="col-md-6">
              <div className="neon-card slide-in-right">
                <h3>For Individuals</h3>
                <ul className="list-unstyled">
                  <li>✓ Early stress detection and prevention</li>
                  <li>✓ Personalized wellness recommendations</li>
                  <li>✓ Improved work-life balance insights</li>
                  <li>✓ Enhanced self-awareness and emotional intelligence</li>
                  <li>✓ Reduced risk of burnout and mental health issues</li>
                </ul>
              </div>
            </div>
            <div className="col-md-6">
              <div className="neon-card slide-in-right" style={{animationDelay: '0.3s'}}>
                <h3>For Organizations</h3>
                <ul className="list-unstyled">
                  <li>✓ 73% reduction in burnout rates</li>
                  <li>✓ 45% increase in team productivity</li>
                  <li>✓ 62% decrease in healthcare costs</li>
                  <li>✓ Enhanced employee retention and satisfaction</li>
                  <li>✓ Data-driven wellness program optimization</li>
                </ul>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Call to Action */}
      <section style={{
        background: 'linear-gradient(135deg, #e4e9d9 0%, #f4f6f2 50%, #e8efda 100%)',
        padding: '4rem 0'
      }}>
        <div className="container text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="neon-text mb-4">Ready to Transform Your Workplace?</h2>
            <p className="lead mb-4">
              Join thousands of organizations already using StressConnect to create 
              healthier, more productive work environments.
            </p>
            <div className="btn-group">
              <Link to="/dashboard" className="btn btn-neon me-3">Try It Now</Link>
              <Link to="/about" className="btn btn-outline-neon">Learn More</Link>
            </div>
            <div style={{
              marginTop: '2rem',
              padding: '1rem',
              background: 'rgba(178, 187, 95, 0.1)',
              borderRadius: '10px',
              display: 'inline-block'
            }}>
              <small style={{color: '#556022'}}>
                🎁 <strong>Free Trial:</strong> Start with a 30-day complimentary assessment for your team
              </small>
            </div>
          </motion.div>
        </div>
      </section>
    </>
  );
}