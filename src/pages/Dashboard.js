import React, { useState } from "react";

export default function Dashboard() {
  const [faceResult, setFaceResult] = useState(null);

  const handleFaceUpload = (e) => {
    const file = e.target.files[0];
    if(file) setFaceResult("Analyzing... (mock result: Stress Level 42%)");
  };

  return (
    <div className="container py-5">
      <h2 className="neon-text text-center">Stress Detection Dashboard</h2>
      
      <div className="row mt-4">
        <div className="col-md-6 neon-card">
          <h4>Facial Stress Detection</h4>
          <input type="file" onChange={handleFaceUpload} className="form-control mb-2"/>
          <button className="btn btn-neon w-100">Open Webcam</button>
          {faceResult && <p className="mt-2">{faceResult}</p>}
        </div>

        <div className="col-md-6 neon-card">
          <h4>Voice Stress Detection</h4>
          <button className="btn btn-neon w-100">Record Voice</button>
        </div>
      </div>

      <div className="row mt-4">
        <div className="col-md-6 neon-card">
          <h4>EEG Data Analysis</h4>
          <input type="file" className="form-control"/>
        </div>
        <div className="col-md-6 neon-card">
          <h4>GSR Data Analysis</h4>
          <input type="file" className="form-control"/>
        </div>
      </div>
    </div>
  );
}
