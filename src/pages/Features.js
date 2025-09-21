import React from "react";

export default function Features() {
  const features = [
    { title: "Facial Stress Detection", desc: "Analyze facial expressions via webcam or photo." },
    { title: "Voice Stress Detection", desc: "Record voice samples to detect stress patterns." },
    { title: "EEG Analysis", desc: "Upload EEG data to assess neurological stress indicators." },
    { title: "GSR Analysis", desc: "Monitor GSR signals to evaluate stress responses." },
  ];

  return (
    <div className="container py-5">
      <h2 className="neon-text text-center mb-4">Features</h2>
      <div className="row">
        {features.map((f, idx) => (
          <div className="col-md-6 mb-4" key={idx}>
            <div className="neon-card">
              <h4>{f.title}</h4>
              <p>{f.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
