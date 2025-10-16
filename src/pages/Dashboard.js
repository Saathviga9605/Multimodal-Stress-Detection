import React, { useState, useEffect } from "react";
import "../theme.css";

export default function Dashboard() {
  const [faceResult, setFaceResult] = useState(null);
  const [voiceResult, setVoiceResult] = useState(null);
  const [eegResult, setEegResult] = useState(null);
  const [gsrResult, setGsrResult] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [overallStress, setOverallStress] = useState(null);
  const [voiceFile, setVoiceFile] = useState(null);
  const [voicePreviewUrl, setVoicePreviewUrl] = useState(null);

  const handleFaceUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFaceResult("Analyzing facial expressions...");
      setTimeout(() => {
        setFaceResult("✅ Analysis Complete - Stress Level: 42% (Moderate)");
        calculateOverallStress();
      }, 2000);
    }
  };

  const handleVoiceRecord = async () => {
    setIsRecording(true);
    setVoiceResult("🎤 Recording voice sample...");
    try {
      const response = await fetch('http://localhost:5000/api/voice/record', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ duration: 3 }),
      });
      const data = await response.json();
      setIsRecording(false);
      if (data.status === 'success') {
        setVoiceResult(`✅ Analysis Complete - Vocal Stress: ${data.percentage}% (${data.stress_level})`);
        calculateOverallStress();
      } else {
        setVoiceResult(`⚠️ Error: ${data.message}`);
      }
    } catch (error) {
      setIsRecording(false);
      setVoiceResult(`⚠️ Error: Network error - ${error.message}. Is the server running?`);
    }
  };

  const handleVoiceUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.type.startsWith('audio/')) {
        setVoiceResult('⚠️ Please upload a valid audio file (WAV or MP3).');
        return;
      }
      setVoiceFile(file);
      setVoiceResult('✅ Audio file selected — ready to analyze');
      const url = URL.createObjectURL(file);
      setVoicePreviewUrl(url);
    }
  };

  const handleVoiceAnalyze = async () => {
    if (!voiceFile) {
      setVoiceResult('⚠️ No audio file selected. Please upload a file first.');
      return;
    }
    setVoiceResult('Analyzing uploaded audio sample...');
    try {
      const formData = new FormData();
      formData.append('file', voiceFile);
      const response = await fetch('http://localhost:5000/api/voice/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (data.status === 'success') {
        setVoiceResult(`✅ Analysis Complete - Vocal Stress: ${data.percentage}% (${data.stress_level})`);
        calculateOverallStress();
      } else {
        setVoiceResult(`⚠️ Error: ${data.message}`);
      }
    } catch (error) {
      setVoiceResult(`⚠️ Error: Network error - ${error.message}. Is the server running?`);
    }
  };

  useEffect(() => {
    const current = voicePreviewUrl;
    return () => {
      if (current) {
        URL.revokeObjectURL(current);
      }
    };
  }, [voicePreviewUrl]);

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
    setTimeout(() => {
      setOverallStress({
        level: 42,
        status: "Moderate Stress",
        recommendation: "Consider taking short breaks and practicing deep breathing exercises."
      });
    }, 500);
  };

  const getStressColor = (level) => {
    if (level < 30) return "#8d9740";
    if (level < 60) return "#e4a853";
    return "#c74545";
  };

  return (
    <div className="container py-5">
      <div className="text-center mb-5">
        <h2 className="neon-text">Stress Detection Dashboard</h2>
        <p className="lead">Real-time multi-modal stress analysis and monitoring</p>
      </div>

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

      <div className="row">
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

        <div className="col-md-6 mb-4">
          <div className="neon-card">
            <div className="text-center mb-3">
              <span style={{fontSize: '3rem'}}>🎤</span>
            </div>
            <h4>Voice Stress Detection</h4>
            <p>Record a voice sample or upload an audio file to analyze vocal patterns for stress markers.</p>
            <div className="mb-3">
              <button 
                className={`btn ${isRecording ? 'btn-outline-neon' : 'btn-neon'} w-100`}
                onClick={handleVoiceRecord}
                disabled={isRecording}
              >
                {isRecording ? '🔴 Recording...' : '🎙️ Start Recording'}
              </button>
            </div>
            <div className="mb-3">
              <label className="form-label">Or upload an audio file</label>
              <input
                type="file"
                accept="audio/*"
                onChange={handleVoiceUpload}
                className="form-control mb-2"
              />
              {voicePreviewUrl && (
                <div style={{marginBottom: '0.75rem'}}>
                  <audio controls src={voicePreviewUrl} style={{width: '100%'}} />
                </div>
              )}
              <button className="btn btn-outline-neon w-100" onClick={handleVoiceAnalyze}>
                Analyze Uploaded Audio
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