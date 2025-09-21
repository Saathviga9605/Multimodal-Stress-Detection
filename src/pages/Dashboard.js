import React, { useState } from "react";
import "../theme.css";

export default function Dashboard() {
  const [faceResult, setFaceResult] = useState(null);
  const [voiceResult, setVoiceResult] = useState(null);
  const [eegResult, setEegResult] = useState(null);
  const [gsrResult, setGsrResult] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [overallStress, setOverallStress] = useState(null);

  const handleFaceUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFaceResult("Analyzing facial expressions...");
      // Simulate analysis
      setTimeout(() => {
        setFaceResult("✅ Analysis Complete - Stress Level: 42% (Moderate)");
        calculateOverallStress();
      }, 2000);
    }
  };

  const handleVoiceRecord = () => {
    setIsRecording(true);
    setVoiceResult("🎤 Recording voice sample...");
    
    setTimeout(() => {
      setIsRecording(false);
      setVoiceResult("✅ Analysis Complete - Vocal Stress: 38% (Low-Moderate)");
      calculateOverallStress();
    }, 3000);
  };

  const handleEEGUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setEegResult("Processing EEG data...");
      setTimeout(() => {
        setEegResult("✅ Analysis Complete - Neural Stress: 55% (Moderate-High)");
        calculateOverallStress();
      }, 2500);
    }
  };

  const handleGSRUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setGsrResult("Analyzing GSR patterns...");
      setTimeout(() => {
        setGsrResult("✅ Analysis Complete - Physiological Stress: 34% (Low)");
        calculateOverallStress();
      }, 1500);
    }
  };

  const calculateOverallStress = () => {
    // Simulate overall stress calculation
    setTimeout(() => {
      setOverallStress({
        level: 42,
        status: "Moderate Stress",
        recommendation: "Consider taking short breaks and practicing deep breathing exercises."
      });
    }, 500);
  };

  const getStressColor = (level) => {
    if (level < 30) return "#8d9740"; // Low - Green
    if (level < 60) return "#e4a853"; // Moderate - Yellow  
    return "#c74545"; // High - Red
  };

  return (
    <div className="container py-5">
      <div className="text-center mb-5">
        <h2 className="neon-text">Stress Detection Dashboard</h2>
        <p className="lead">Real-time multi-modal stress analysis and monitoring</p>
      </div>

      {/* Overall Stress Display */}
      {overallStress && (
        <div className="row mb-5">
          <div className="col-12">
            <div className="neon-card text-center" style={{
              background: `linear-gradient(135deg, rgba(178, 187, 95, 0.1), rgba(178, 187, 95, 0.05))`
            }}>
              <h3>Overall Stress Assessment</h3>
              <div style={{
                fontSize: '4rem',
                fontWeight: 'bold',
                color: getStressColor(overallStress.level),
                textShadow: `0 0 20px ${getStressColor(overallStress.level)}40`
              }}>
                {overallStress.level}%
              </div>
              <h4 style={{color: getStressColor(overallStress.level)}}>
                {overallStress.status}
              </h4>
              <p style={{
                background: 'rgba(178, 187, 95, 0.1)',
                padding: '1rem',
                borderRadius: '8px',
                marginTop: '1rem'
              }}>
                <strong>Recommendation:</strong> {overallStress.recommendation}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Detection Modules */}
      <div className="row">
        {/* Facial Stress Detection */}
        <div className="col-md-6 mb-4">
          <div className="neon-card">
            <div className="text-center mb-3">
              <span style={{fontSize: '3rem'}}>📸</span>
            </div>
            <h4>Facial Stress Detection</h4>
            <p>Upload a photo or use your webcam to analyze facial expressions for stress indicators.</p>
            
            <div className="mb-3">
              <input 
                type="file" 
                onChange={handleFaceUpload} 
                className="form-control mb-2"
                accept="image/*"
              />
              <button className="btn btn-neon w-100" onClick={() => alert('Webcam feature coming soon!')}>
                📹 Open Webcam
              </button>
            </div>
            
            {faceResult && (
              <div style={{
                background: 'rgba(178, 187, 95, 0.1)',
                padding: '1rem',
                borderRadius: '8px',
                marginTop: '1rem'
              }}>
                <strong>Result:</strong> {faceResult}
              </div>
            )}
          </div>
        </div>

        {/* Voice Stress Detection */}
        <div className="col-md-6 mb-4">
          <div className="neon-card">
            <div className="text-center mb-3">
              <span style={{fontSize: '3rem'}}>🎤</span>
            </div>
            <h4>Voice Stress Detection</h4>
            <p>Record a voice sample to analyze vocal patterns and stress markers in speech.</p>
            
            <div className="mb-3">
              <button 
                className={`btn ${isRecording ? 'btn-outline-neon' : 'btn-neon'} w-100`}
                onClick={handleVoiceRecord}
                disabled={isRecording}
              >
                {isRecording ? '🔴 Recording...' : '🎙️ Start Recording'}
              </button>
            </div>
            
            {voiceResult && (
              <div style={{
                background: 'rgba(178, 187, 95, 0.1)',
                padding: '1rem',
                borderRadius: '8px',
                marginTop: '1rem'
              }}>
                <strong>Result:</strong> {voiceResult}
              </div>
            )}
          </div>
        </div>

        {/* EEG Data Analysis */}
        <div className="col-md-6 mb-4">
          <div className="neon-card">
            <div className="text-center mb-3">
              <span style={{fontSize: '3rem'}}>🧠</span>
            </div>
            <h4>EEG Data Analysis</h4>
            <p>Upload EEG data files to analyze brainwave patterns and neurological stress indicators.</p>
            
            <div className="mb-3">
              <input 
                type="file" 
                onChange={handleEEGUpload}
                className="form-control"
                accept=".edf,.csv,.txt"
              />
              <small style={{color: '#556022'}}>
                Supported formats: EDF, CSV, TXT
              </small>
            </div>
            
            {eegResult && (
              <div style={{
                background: 'rgba(178, 187, 95, 0.1)',
                padding: '1rem',
                borderRadius: '8px',
                marginTop: '1rem'
              }}>
                <strong>Result:</strong> {eegResult}
              </div>
            )}
          </div>
        </div>

        {/* GSR Data Analysis */}
        <div className="col-md-6 mb-4">
          <div className="neon-card">
            <div className="text-center mb-3">
              <span style={{fontSize: '3rem'}}>⚡</span>
            </div>
            <h4>GSR Data Analysis</h4>
            <p>Monitor Galvanic Skin Response data to evaluate physiological stress responses.</p>
            
            <div className="mb-3">
              <input 
                type="file" 
                onChange={handleGSRUpload}
                className="form-control"
                accept=".csv,.txt,.json"
              />
              <small style={{color: '#556022'}}>
                Supported formats: CSV, TXT, JSON
              </small>
            </div>
            
            {gsrResult && (
              <div style={{
                background: 'rgba(178, 187, 95, 0.1)',
                padding: '1rem',
                borderRadius: '8px',
                marginTop: '1rem'
              }}>
                <strong>Result:</strong> {gsrResult}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="row mt-5">
        <div className="col-12">
          <div className="neon-card">
            <h3 className="text-center mb-4">How to Use the Dashboard</h3>
            <div className="row">
              <div className="col-md-6">
                <h4>Getting Started</h4>
                <ul className="list-unstyled">
                  <li>1. Choose one or more detection methods</li>
                  <li>2. Upload your data or use real-time capture</li>
                  <li>3. Wait for analysis to complete</li>
                  <li>4. Review your stress assessment results</li>
                  <li>5. Follow personalized recommendations</li>
                </ul>
              </div>
              <div className="col-md-6">
                <h4>Best Practices</h4>
                <ul className="list-unstyled">
                  <li>• Use multiple detection methods for accuracy</li>
                  <li>• Take measurements in consistent environments</li>
                  <li>• Regular monitoring provides better insights</li>
                  <li>• Follow up on high stress readings</li>
                  <li>• Share results with wellness coordinators</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}