// import React, { useState, useEffect } from "react";
// import "../theme.css";

// export default function Dashboard() {
//   const [faceResult, setFaceResult] = useState(null);
//   const [voiceResult, setVoiceResult] = useState(null);
//   const [eegResult, setEegResult] = useState(null);
//   const [gsrResult, setGsrResult] = useState(null);
//   const [isRecording, setIsRecording] = useState(false);
//   const [overallStress, setOverallStress] = useState(null);
//   const [voiceFile, setVoiceFile] = useState(null);
//   const [voicePreviewUrl, setVoicePreviewUrl] = useState(null);

//   const handleFaceUpload = async (e) => {
//     const file = e.target.files[0];
//     if (file) {
//       if (!file.type.startsWith('image/')) {
//         setFaceResult('⚠️ Please upload a valid image file (JPG, JPEG, PNG).');
//         return;
//       }
//       setFaceResult("Analyzing facial expressions...");
//       try {
//         const formData = new FormData();
//         formData.append('file', file);
//         const response = await fetch('http://localhost:5000/api/face/upload', {
//           method: 'POST',
//           body: formData,
//         });
//         const data = await response.json();
//         if (data.status === 'success') {
//           setFaceResult(`✅ Analysis Complete - Facial Stress: ${data.percentage}% (${data.stress_level})`);
//           calculateOverallStress();
//         } else {
//           setFaceResult(`⚠️ Error: ${data.message}`);
//         }
//       } catch (error) {
//         setFaceResult(`⚠️ Error: Network error - ${error.message}. Is the server running?`);
//       }
//     }
//   };

//   const handleVoiceRecord = async () => {
//     setIsRecording(true);
//     setVoiceResult("🎤 Recording voice sample...");
//     try {
//       const response = await fetch('http://localhost:5000/api/voice/record', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ duration: 3 }),
//       });
//       const data = await response.json();
//       setIsRecording(false);
//       if (data.status === 'success') {
//         setVoiceResult(`✅ Analysis Complete - Vocal Stress: ${data.percentage}% (${data.stress_level})`);
//         calculateOverallStress();
//       } else {
//         setVoiceResult(`⚠️ Error: ${data.message}`);
//       }
//     } catch (error) {
//       setIsRecording(false);
//       setVoiceResult(`⚠️ Error: Network error - ${error.message}. Is the server running?`);
//     }
//   };

//   const handleVoiceUpload = (e) => {
//     const file = e.target.files[0];
//     if (file) {
//       if (!file.type.startsWith('audio/')) {
//         setVoiceResult('⚠️ Please upload a valid audio file (WAV or MP3).');
//         return;
//       }
//       setVoiceFile(file);
//       setVoiceResult('✅ Audio file selected — ready to analyze');
//       const url = URL.createObjectURL(file);
//       setVoicePreviewUrl(url);
//     }
//   };

//   const handleVoiceAnalyze = async () => {
//     if (!voiceFile) {
//       setVoiceResult('⚠️ No audio file selected. Please upload a file first.');
//       return;
//     }
//     setVoiceResult('Analyzing uploaded audio sample...');
//     try {
//       const formData = new FormData();
//       formData.append('file', voiceFile);
//       const response = await fetch('http://localhost:5000/api/voice/upload', {
//         method: 'POST',
//         body: formData,
//       });
//       const data = await response.json();
//       if (data.status === 'success') {
//         setVoiceResult(`✅ Analysis Complete - Vocal Stress: ${data.percentage}% (${data.stress_level})`);
//         calculateOverallStress();
//       } else {
//         setVoiceResult(`⚠️ Error: ${data.message}`);
//       }
//     } catch (error) {
//       setVoiceResult(`⚠️ Error: Network error - ${error.message}. Is the server running?`);
//     }
//   };

//   useEffect(() => {
//     const current = voicePreviewUrl;
//     return () => {
//       if (current) {
//         URL.revokeObjectURL(current);
//       }
//     };
//   }, [voicePreviewUrl]);

//   const handleEEGUpload = (e) => {
//     const file = e.target.files[0];
//     if (file) {
//       setEegResult("Processing EEG data...");
//       setTimeout(() => {
//         setEegResult("✅ Analysis Complete - Neural Stress: 55% (Moderate-High)");
//         calculateOverallStress();
//       }, 2500);
//     }
//   };

//   const handleGSRUpload = (e) => {
//     const file = e.target.files[0];
//     if (file) {
//       setGsrResult("Analyzing GSR patterns...");
//       setTimeout(() => {
//         setGsrResult("✅ Analysis Complete - Physiological Stress: 34% (Low)");
//         calculateOverallStress();
//       }, 1500);
//     }
//   };

//   const calculateOverallStress = () => {
//     setTimeout(() => {
//       setOverallStress({
//         level: 42,
//         status: "Moderate Stress",
//         recommendation: "Consider taking short breaks and practicing deep breathing exercises."
//       });
//     }, 500);
//   };

//   const getStressColor = (level) => {
//     if (level < 30) return "#8d9740";
//     if (level < 60) return "#e4a853";
//     return "#c74545";
//   };

//   return (
//     <div className="container py-5">
//       <div className="text-center mb-5">
//         <h2 className="neon-text">Stress Detection Dashboard</h2>
//         <p className="lead">Real-time multi-modal stress analysis and monitoring</p>
//       </div>

//       {overallStress && (
//         <div className="row mb-5">
//           <div className="col-12">
//             <div className="neon-card text-center" style={{
//               background: `linear-gradient(135deg, rgba(178, 187, 95, 0.1), rgba(178, 187, 95, 0.05))`
//             }}>
//               <h3>Overall Stress Assessment</h3>
//               <div style={{
//                 fontSize: '4rem',
//                 fontWeight: 'bold',
//                 color: getStressColor(overallStress.level),
//                 textShadow: `0 0 20px ${getStressColor(overallStress.level)}40`
//               }}>
//                 {overallStress.level}%
//               </div>
//               <h4 style={{color: getStressColor(overallStress.level)}}>
//                 {overallStress.status}
//               </h4>
//               <p style={{
//                 background: 'rgba(178, 187, 95, 0.1)',
//                 padding: '1rem',
//                 borderRadius: '8px',
//                 marginTop: '1rem'
//               }}>
//                 <strong>Recommendation:</strong> {overallStress.recommendation}
//               </p>
//             </div>
//           </div>
//         </div>
//       )}

//       <div className="row">
//         <div className="col-md-6 mb-4">
//           <div className="neon-card">
//             <div className="text-center mb-3">
//               <span style={{fontSize: '3rem'}}>📸</span>
//             </div>
//             <h4>Facial Stress Detection</h4>
//             <p>Upload a photo or use your webcam to analyze facial expressions for stress indicators.</p>
//             <div className="mb-3">
//               <input 
//                 type="file" 
//                 onChange={handleFaceUpload} 
//                 className="form-control mb-2"
//                 accept="image/*"
//               />
//               <button className="btn btn-neon w-100" onClick={() => alert('Webcam feature coming soon!')}>
//                 📹 Open Webcam
//               </button>
//             </div>
//             {faceResult && (
//               <div style={{
//                 background: 'rgba(178, 187, 95, 0.1)',
//                 padding: '1rem',
//                 borderRadius: '8px',
//                 marginTop: '1rem'
//               }}>
//                 <strong>Result:</strong> {faceResult}
//               </div>
//             )}
//           </div>
//         </div>

//         <div className="col-md-6 mb-4">
//           <div className="neon-card">
//             <div className="text-center mb-3">
//               <span style={{fontSize: '3rem'}}>🎤</span>
//             </div>
//             <h4>Voice Stress Detection</h4>
//             <p>Record a voice sample or upload an audio file to analyze vocal patterns for stress markers.</p>
//             <div className="mb-3">
//               <button 
//                 className={`btn ${isRecording ? 'btn-outline-neon' : 'btn-neon'} w-100`}
//                 onClick={handleVoiceRecord}
//                 disabled={isRecording}
//               >
//                 {isRecording ? '🔴 Recording...' : '🎙️ Start Recording'}
//               </button>
//             </div>
//             <div className="mb-3">
//               <label className="form-label">Or upload an audio file</label>
//               <input
//                 type="file"
//                 accept="audio/*"
//                 onChange={handleVoiceUpload}
//                 className="form-control mb-2"
//               />
//               {voicePreviewUrl && (
//                 <div style={{marginBottom: '0.75rem'}}>
//                   <audio controls src={voicePreviewUrl} style={{width: '100%'}} />
//                 </div>
//               )}
//               <button className="btn btn-outline-neon w-100" onClick={handleVoiceAnalyze}>
//                 Analyze Uploaded Audio
//               </button>
//             </div>
//             {voiceResult && (
//               <div style={{
//                 background: 'rgba(178, 187, 95, 0.1)',
//                 padding: '1rem',
//                 borderRadius: '8px',
//                 marginTop: '1rem'
//               }}>
//                 <strong>Result:</strong> {voiceResult}
//               </div>
//             )}
//           </div>
//         </div>

//         <div className="col-md-6 mb-4">
//           <div className="neon-card">
//             <div className="text-center mb-3">
//               <span style={{fontSize: '3rem'}}>🧠</span>
//             </div>
//             <h4>EEG Data Analysis</h4>
//             <p>Upload EEG data files to analyze brainwave patterns and neurological stress indicators.</p>
//             <div className="mb-3">
//               <input 
//                 type="file" 
//                 onChange={handleEEGUpload}
//                 className="form-control"
//                 accept=".edf,.csv,.txt"
//               />
//               <small style={{color: '#556022'}}>
//                 Supported formats: EDF, CSV, TXT
//               </small>
//             </div>
//             {eegResult && (
//               <div style={{
//                 background: 'rgba(178, 187, 95, 0.1)',
//                 padding: '1rem',
//                 borderRadius: '8px',
//                 marginTop: '1rem'
//               }}>
//                 <strong>Result:</strong> {eegResult}
//               </div>
//             )}
//           </div>
//         </div>

//         <div className="col-md-6 mb-4">
//           <div className="neon-card">
//             <div className="text-center mb-3">
//               <span style={{fontSize: '3rem'}}>⚡</span>
//             </div>
//             <h4>GSR Data Analysis</h4>
//             <p>Monitor Galvanic Skin Response data to evaluate physiological stress responses.</p>
//             <div className="mb-3">
//               <input 
//                 type="file" 
//                 onChange={handleGSRUpload}
//                 className="form-control"
//                 accept=".csv,.txt,.json"
//               />
//               <small style={{color: '#556022'}}>
//                 Supported formats: CSV, TXT, JSON
//               </small>
//             </div>
//             {gsrResult && (
//               <div style={{
//                 background: 'rgba(178, 187, 95, 0.1)',
//                 padding: '1rem',
//                 borderRadius: '8px',
//                 marginTop: '1rem'
//               }}>
//                 <strong>Result:</strong> {gsrResult}
//               </div>
//             )}
//           </div>
//         </div>
//       </div>

//       <div className="row mt-5">
//         <div className="col-12">
//           <div className="neon-card">
//             <h3 className="text-center mb-4">How to Use the Dashboard</h3>
//             <div className="row">
//               <div className="col-md-6">
//                 <h4>Getting Started</h4>
//                 <ul className="list-unstyled">
//                   <li>1. Choose one or more detection methods</li>
//                   <li>2. Upload your data or use real-time capture</li>
//                   <li>3. Wait for analysis to complete</li>
//                   <li>4. Review your stress assessment results</li>
//                   <li>5. Follow personalized recommendations</li>
//                 </ul>
//               </div>
//               <div className="col-md-6">
//                 <h4>Best Practices</h4>
//                 <ul className="list-unstyled">
//                   <li>• Use multiple detection methods for accuracy</li>
//                   <li>• Take measurements in consistent environments</li>
//                   <li>• Regular monitoring provides better insights</li>
//                   <li>• Follow up on high stress readings</li>
//                   <li>• Share results with wellness coordinators</li>
//                 </ul>
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }


import React, { useState, useRef, useEffect, useMemo } from "react";
import "../theme.css";
import AnalysisPanel from "../components/AnalysisPanel";
import InsightCards from "../components/InsightCards";
import CopilotMessage from "../components/CopilotMessage";
import GamePanel from "../components/GamePanel";
import RewardSystem from "../components/RewardSystem";
import StressChatbot from "../components/StressChatbot";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

export default function Dashboard() {
  // File states
  const [faceImage, setFaceImage] = useState(null);
  const [facePreview, setFacePreview] = useState(null);
  const [voiceFile, setVoiceFile] = useState(null);
  const [voicePreviewUrl, setVoicePreviewUrl] = useState(null);
  const [eegData, setEegData] = useState("");
  const [gsrData, setGsrData] = useState("");
  const [eegFile, setEegFile] = useState(null);
  const [gsrFile, setGsrFile] = useState(null);
  const [eegPreviewData, setEegPreviewData] = useState([]);
  const [eegPreviewKeys, setEegPreviewKeys] = useState([]);
  const [gsrPreviewData, setGsrPreviewData] = useState([]);
  const [gsrPreviewKeys, setGsrPreviewKeys] = useState([]);
  const [liveFaceResult, setLiveFaceResult] = useState(null);
  const [liveVoiceResult, setLiveVoiceResult] = useState(null);
  const [isMicRecording, setIsMicRecording] = useState(false);
  const [micWaveformData, setMicWaveformData] = useState([]);
  
  // UI states
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [webcamActive, setWebcamActive] = useState(false);

  // Result interaction states
  const [stressLevel, setStressLevel] = useState("Moderate");
  const [isGameActive, setIsGameActive] = useState(false);
  const [selectedActivity, setSelectedActivity] = useState(null);
  const [recoveryScore, setRecoveryScore] = useState(72);
  const [calmStreak, setCalmStreak] = useState(8);
  const [reward, setReward] = useState(null);

  // Muse realtime states
  const [museDuration, setMuseDuration] = useState(20);
  const [museFilename, setMuseFilename] = useState("C:\\Musedata\\eeg_session.csv");
  const [museCollecting, setMuseCollecting] = useState(false);
  const [musePoints, setMusePoints] = useState([]);
  const [museSessionError, setMuseSessionError] = useState(null);
  const [museElapsed, setMuseElapsed] = useState(0);
  
  // Refs for webcam
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const micStreamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const waveformFrameRef = useRef(null);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (voicePreviewUrl) URL.revokeObjectURL(voicePreviewUrl);
      if (facePreview) URL.revokeObjectURL(facePreview);
      stopWebcam();
      stopMicRecording();
    };
  }, [voicePreviewUrl, facePreview]);

  const parseDelimitedSeries = (text, keyName = "value") => {
    const values = (text || "")
      .split(/[\s,;]+/)
      .map((item) => Number(item.trim()))
      .filter((item) => Number.isFinite(item));

    return values.slice(0, 300).map((value, index) => ({ index, [keyName]: value }));
  };

  const parseSignalCsvForPreview = (file, preferredHeaders = []) =>
    new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const text = String(reader.result || "");
          const rows = text
            .split(/\r?\n/)
            .map((row) => row.trim())
            .filter(Boolean)
            .slice(0, 1200);

          if (rows.length === 0) {
            resolve({ data: [], keys: [] });
            return;
          }

          const firstRow = rows[0].split(",").map((cell) => cell.trim());
          const hasHeader = firstRow.some((cell) => Number.isNaN(Number(cell)));
          const headers = hasHeader ? firstRow : firstRow.map((_, index) => `col_${index}`);
          const bodyRows = hasHeader ? rows.slice(1) : rows;

          const normalizedPreferred = preferredHeaders.map((item) => item.toLowerCase());
          const selectedIndexes = headers
            .map((header, index) => ({ header, index }))
            .filter(({ header }) => {
              const normalized = header.toLowerCase().replace(/\s+/g, "");
              if (normalized.includes("timestamp") || normalized === "time") return false;
              return (
                normalizedPreferred.length === 0 ||
                normalizedPreferred.includes(normalized) ||
                normalizedPreferred.includes(header.toLowerCase())
              );
            })
            .map((entry) => entry.index);

          const fallBackIndexes =
            selectedIndexes.length > 0
              ? selectedIndexes
              : headers
                  .map((header, index) => ({ header, index }))
                  .filter(({ header }) => !header.toLowerCase().includes("timestamp"))
                  .map((entry) => entry.index)
                  .slice(0, 4);

          const safeIndexes = fallBackIndexes.slice(0, 5);
          const safeKeys = safeIndexes.map((idx) => headers[idx].replace(/\s+/g, "") || `col_${idx}`);

          const points = [];
          for (let i = 0; i < bodyRows.length && points.length < 280; i += 1) {
            const cells = bodyRows[i].split(",").map((cell) => cell.trim());
            const point = { index: points.length };
            let hasAny = false;

            safeIndexes.forEach((sourceIdx, kIdx) => {
              const value = Number(cells[sourceIdx]);
              if (Number.isFinite(value)) {
                point[safeKeys[kIdx]] = value;
                hasAny = true;
              }
            });

            if (hasAny) points.push(point);
          }

          resolve({ data: points, keys: safeKeys });
        } catch (_err) {
          resolve({ data: [], keys: [] });
        }
      };

      reader.onerror = () => resolve({ data: [], keys: [] });
      reader.readAsText(file);
    });

  const stopMicRecording = () => {
    if (waveformFrameRef.current) {
      cancelAnimationFrame(waveformFrameRef.current);
      waveformFrameRef.current = null;
    }

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop();
    }

    if (micStreamRef.current) {
      micStreamRef.current.getTracks().forEach((track) => track.stop());
      micStreamRef.current = null;
    }

    if (audioContextRef.current) {
      audioContextRef.current.close().catch(() => {});
      audioContextRef.current = null;
    }

    analyserRef.current = null;
    setIsMicRecording(false);
  };

  const analyzeVoiceFile = async (fileToAnalyze) => {
    try {
      const formData = new FormData();
      formData.append("file", fileToAnalyze);
      const response = await fetch("/api/voice/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (data.status === "success") {
        setLiveVoiceResult(data);
      } else {
        setError(data.message || "Live voice analysis failed.");
      }
    } catch (err) {
      setError(`Live voice analysis failed: ${err.message}`);
    }
  };

  const startMicRecording = async () => {
    try {
      setError(null);
      setLiveVoiceResult(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      micStreamRef.current = stream;

      const audioContext = new window.AudioContext();
      audioContextRef.current = audioContext;
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 256;
      analyserRef.current = analyser;

      const source = audioContext.createMediaStreamSource(stream);
      source.connect(analyser);

      const updateWaveform = () => {
        if (!analyserRef.current) return;
        const bufferLength = analyserRef.current.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        analyserRef.current.getByteTimeDomainData(dataArray);
        const downSampled = Array.from(dataArray)
          .filter((_, idx) => idx % 4 === 0)
          .map((value, idx) => ({ index: idx, amplitude: (value - 128) / 128 }));
        setMicWaveformData(downSampled);
        waveformFrameRef.current = requestAnimationFrame(updateWaveform);
      };
      updateWaveform();

      const mimeType = MediaRecorder.isTypeSupported("audio/webm")
        ? "audio/webm"
        : MediaRecorder.isTypeSupported("audio/ogg")
        ? "audio/ogg"
        : "";
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        const recordedType = recorder.mimeType || "audio/webm";
        const extension = recordedType.includes("ogg") ? "ogg" : "webm";
        const blob = new Blob(audioChunksRef.current, { type: recordedType });
        const file = new File([blob], `live-recording.${extension}`, { type: recordedType });

        setVoiceFile(file);
        const url = URL.createObjectURL(blob);
        setVoicePreviewUrl(url);
        await analyzeVoiceFile(file);
      };

      recorder.start();
      setIsMicRecording(true);
    } catch (err) {
      setError(`Could not start microphone recording: ${err.message}`);
      stopMicRecording();
    }
  };

  const analyzeLiveWebcam = async () => {
    if (!videoRef.current || !canvasRef.current) {
      setError("Webcam is not active. Please start webcam first.");
      return;
    }

    try {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0);

      const base64Image = canvas.toDataURL("image/jpeg", 0.9);
      const response = await fetch("/api/webcam/capture", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64Image }),
      });

      const data = await response.json();
      if (data.status === "success") {
        setLiveFaceResult(data);
      } else {
        setError(data.message || "Live webcam analysis failed.");
      }
    } catch (err) {
      setError(`Live webcam analysis failed: ${err.message}`);
    }
  };

  const handleFaceUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please upload a valid image file (JPG, JPEG, PNG)');
        return;
      }
      setFaceImage(file);
      setFacePreview(URL.createObjectURL(file));
      setError(null);
    }
  };

  const handleVoiceUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.type.startsWith('audio/')) {
        setError('Please upload a valid audio file (WAV, MP3)');
        return;
      }
      setVoiceFile(file);
      setVoicePreviewUrl(URL.createObjectURL(file));
      setError(null);
    }
  };

  const handleEegTextChange = (value) => {
    setEegData(value);
    const preview = parseDelimitedSeries(value, "EEG");
    setEegPreviewData(preview);
    setEegPreviewKeys(preview.length > 0 ? ["EEG"] : []);
  };

  const handleGsrTextChange = (value) => {
    setGsrData(value);
    const preview = parseDelimitedSeries(value, "GSR");
    setGsrPreviewData(preview);
    setGsrPreviewKeys(preview.length > 0 ? ["GSR"] : []);
  };

  const handleEegFileUpload = async (file) => {
    setEegFile(file || null);
    if (!file) {
      setEegPreviewData([]);
      setEegPreviewKeys([]);
      return;
    }

    const preview = await parseSignalCsvForPreview(file, ["tp9", "af7", "af8", "tp10", "rightaux", "right aux"]);
    setEegPreviewData(preview.data);
    setEegPreviewKeys(preview.keys);
  };

  const handleGsrFileUpload = async (file) => {
    setGsrFile(file || null);
    if (!file) {
      setGsrPreviewData([]);
      setGsrPreviewKeys([]);
      return;
    }

    const preview = await parseSignalCsvForPreview(file, []);
    setGsrPreviewData(preview.data);
    setGsrPreviewKeys(preview.keys.slice(0, 2));
  };

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setWebcamActive(true);
      }
    } catch (err) {
      setError('Could not access webcam: ' + err.message);
    }
  };

  const stopWebcam = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setWebcamActive(false);
  };

  const captureWebcam = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      
      canvas.toBlob((blob) => {
        const file = new File([blob], 'webcam-capture.jpg', { type: 'image/jpeg' });
        setFaceImage(file);
        setFacePreview(URL.createObjectURL(file));
        stopWebcam();
      }, 'image/jpeg');
    }
  };

  const analyzeMultimodal = async () => {
    if (!faceImage && !voiceFile && !eegData && !gsrData && !eegFile && !gsrFile) {
      setError('Please provide at least one input (image, audio, EEG, or GSR data)');
      return;
    }

    setAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      
      if (faceImage) formData.append('face_image', faceImage);
      if (voiceFile) formData.append('voice_audio', voiceFile);
      if (eegData) formData.append('eeg_data', eegData);
      if (gsrData) formData.append('gsr_data', gsrData);
      if (eegFile) formData.append('eeg_file', eegFile);
      if (gsrFile) formData.append('gsr_file', gsrFile);

      const response = await fetch('/api/multimodal/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.status === 'success') {
        setResult(data);
      } else {
        setError(data.message || 'Analysis failed');
      }
    } catch (err) {
      setError('Network error: ' + err.message + '. Is the server running on port 5000?');
    } finally {
      setAnalyzing(false);
    }
  };

  const pollMuseStatus = async () => {
    try {
      const response = await fetch('/api/muse/status?limit=280');
      const data = await response.json();
      if (data.status !== 'success') return;

      setMuseCollecting(Boolean(data.collecting));
      setMuseElapsed(Number(data.elapsed_seconds || 0));
      setMusePoints(Array.isArray(data.points) ? data.points : []);

      if (data.error) {
        setMuseSessionError(data.error);
      }

      if (data.prediction && data.prediction.status === 'success') {
        setResult(data.prediction);
      }
    } catch (err) {
      setMuseSessionError('Could not poll Muse status: ' + err.message);
    }
  };

  const startMuseCapture = async () => {
    setMuseSessionError(null);
    try {
      const response = await fetch('/api/muse/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          duration: Number(museDuration),
          filename: museFilename,
        }),
      });
      const data = await response.json();
      if (data.status === 'success') {
        setMuseCollecting(true);
        setMuseElapsed(0);
        setMusePoints([]);
      } else {
        setMuseSessionError(data.message || 'Could not start Muse recording.');
      }
    } catch (err) {
      setMuseSessionError('Could not start Muse recording: ' + err.message);
    }
  };

  const stopMuseCapture = async () => {
    try {
      await fetch('/api/muse/stop', { method: 'POST' });
      setMuseCollecting(false);
      await pollMuseStatus();
    } catch (err) {
      setMuseSessionError('Could not stop Muse recording: ' + err.message);
    }
  };

  useEffect(() => {
    let timer = null;
    if (museCollecting) {
      timer = setInterval(() => {
        pollMuseStatus();
      }, 1000);
    }

    return () => {
      if (timer) clearInterval(timer);
    };
  }, [museCollecting]);

  const clearAll = () => {
    setFaceImage(null);
    setFacePreview(null);
    setVoiceFile(null);
    setVoicePreviewUrl(null);
    setEegData("");
    setGsrData("");
    setEegFile(null);
    setGsrFile(null);
    setResult(null);
    setError(null);
    setStressLevel("Moderate");
    setIsGameActive(false);
    setSelectedActivity(null);
    setRecoveryScore(72);
    setCalmStreak(8);
    setReward(null);
    setMusePoints([]);
    setMuseSessionError(null);
    setMuseElapsed(0);
    setEegPreviewData([]);
    setEegPreviewKeys([]);
    setGsrPreviewData([]);
    setGsrPreviewKeys([]);
    setLiveFaceResult(null);
    setLiveVoiceResult(null);
    setMicWaveformData([]);
    stopWebcam();
    stopMicRecording();
  };

  const getStressColor = (percentage) => {
    if (percentage < 30) return "#8d9740";
    if (percentage < 60) return "#e4a853";
    return "#c74545";
  };

  const getRecommendation = (level) => {
    switch(level) {
      case "Low":
        return "You're doing well! Maintain your current stress management practices.";
      case "Moderate":
        return "Consider taking short breaks and practicing deep breathing exercises.";
      case "High":
        return "High stress detected. Consider speaking with a wellness professional and taking immediate breaks.";
      default:
        return "Continue monitoring your stress levels regularly.";
    }
  };

  useEffect(() => {
    if (!result) return;

    const nextStressLevel = result.stress_level || "Moderate";
    const baseRecovery =
      nextStressLevel === "High" ? 72 : nextStressLevel === "Moderate" ? 79 : 88;

    setStressLevel(nextStressLevel);
    setIsGameActive(false);
    setSelectedActivity(null);
    setRecoveryScore(baseRecovery);
    setCalmStreak(8);
    setReward(null);
  }, [result]);

  const handleActivityComplete = ({ activityName, reducedBy, scoreBoost, streakBoost }) => {
    setRecoveryScore((prev) => {
      const next = Math.min(100, prev + scoreBoost);
      setReward({
        activityName,
        reducedBy,
        from: prev,
        to: next,
      });
      return next;
    });
    setCalmStreak((prev) => prev + streakBoost);
  };

  const resultVisuals = useMemo(() => {
    if (!result) {
      return {
        modalityBars: [],
        radarMetrics: [],
        insightMetrics: { agreement: 0, completeness: 0, riskIndex: 0, resilienceIndex: 0 },
      };
    }

    const pred = result.individual_predictions || {};
    const modalities = [
      { name: "Facial", key: "facial", value: pred.facial },
      { name: "Voice", key: "voice", value: pred.voice },
      { name: "Physio", key: "physiological", value: pred.physiological },
    ];

    const activeValues = modalities
      .map((item) => item.value)
      .filter((value) => value !== null && value !== undefined)
      .map((value) => Number(value) * 100);

    const mean = activeValues.length
      ? activeValues.reduce((sum, value) => sum + value, 0) / activeValues.length
      : 0;
    const variance = activeValues.length
      ? activeValues.reduce((sum, value) => sum + Math.pow(value - mean, 2), 0) / activeValues.length
      : 0;
    const stdDev = Math.sqrt(variance);

    const agreement = Math.max(0, Math.min(100, 100 - stdDev));
    const completeness = (activeValues.length / 3) * 100;
    const riskIndex = Math.max(0, Math.min(100, Number(result.stress_probability || 0) * 100));
    const resilienceIndex = Math.max(0, Math.min(100, 100 - riskIndex + (agreement * 0.2)));

    return {
      modalityBars: modalities
        .filter((item) => item.value !== null && item.value !== undefined)
        .map((item) => ({
          modality: item.name,
          stress: Number(item.value) * 100,
          calm: 100 - Number(item.value) * 100,
        })),
      radarMetrics: [
        { metric: "Risk", value: riskIndex },
        { metric: "Agreement", value: agreement },
        { metric: "Coverage", value: completeness },
        { metric: "Resilience", value: resilienceIndex },
      ],
      insightMetrics: {
        agreement,
        completeness,
        riskIndex,
        resilienceIndex,
      },
    };
  }, [result]);

  return (
    <div className="container py-5">
      <div className="text-center mb-5">
        <h2 className="neon-text">Multimodal Stress Detection</h2>
        <p className="lead">Intelligent stress analysis using facial, vocal, and physiological indicators</p>
      </div>

      {/* Error Display */}
      {error && (
        <div className="row mb-4">
          <div className="col-12">
            <div style={{
              background: 'rgba(199, 69, 69, 0.1)',
              border: '2px solid #c74545',
              borderRadius: '8px',
              padding: '1rem',
              color: '#c74545'
            }}>
              <strong>⚠️ Error:</strong> {error}
            </div>
          </div>
        </div>
      )}

      {/* Result Display */}
      {result && (
        <div className="row mb-5">
          <div className="col-12">
            <div className="neon-card text-center" style={{
              background: `linear-gradient(135deg, rgba(178, 187, 95, 0.1), rgba(178, 187, 95, 0.05))`
            }}>
              <h3>Overall Stress Assessment</h3>
              <div style={{
                fontSize: '4rem',
                fontWeight: 'bold',
                color: getStressColor(result.percentage),
                textShadow: `0 0 20px ${getStressColor(result.percentage)}40`
              }}>
                {result.percentage.toFixed(1)}%
              </div>
              <h4 style={{color: getStressColor(result.percentage)}}>
                {result.stress_level} Stress - {result.predicted_class}
              </h4>
              <div style={{
                display: 'flex',
                justifyContent: 'center',
                gap: '1rem',
                margin: '1.5rem 0',
                flexWrap: 'wrap'
              }}>
                <div style={{
                  background: 'rgba(178, 187, 95, 0.15)',
                  padding: '0.75rem 1.5rem',
                  borderRadius: '8px'
                }}>
                  <small style={{color: '#556022'}}>Confidence</small>
                  <div style={{fontSize: '1.25rem', fontWeight: 'bold'}}>
                    {(result.confidence * 100).toFixed(1)}%
                  </div>
                </div>
                <div style={{
                  background: 'rgba(178, 187, 95, 0.15)',
                  padding: '0.75rem 1.5rem',
                  borderRadius: '8px'
                }}>
                  <small style={{color: '#556022'}}>Stress Probability</small>
                  <div style={{fontSize: '1.25rem', fontWeight: 'bold'}}>
                    {(result.stress_probability * 100).toFixed(1)}%
                  </div>
                </div>
                <div style={{
                  background: 'rgba(178, 187, 95, 0.15)',
                  padding: '0.75rem 1.5rem',
                  borderRadius: '8px'
                }}>
                  <small style={{color: '#556022'}}>No Stress Probability</small>
                  <div style={{fontSize: '1.25rem', fontWeight: 'bold'}}>
                    {(result.no_stress_probability * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))',
                gap: '0.75rem',
                marginBottom: '1rem'
              }}>
                <div className="result-panel-card">
                  <small>Agreement Score</small>
                  <div style={{ fontSize: '1.3rem', fontWeight: 700 }}>{resultVisuals.insightMetrics.agreement.toFixed(1)}%</div>
                </div>
                <div className="result-panel-card">
                  <small>Modality Coverage</small>
                  <div style={{ fontSize: '1.3rem', fontWeight: 700 }}>{resultVisuals.insightMetrics.completeness.toFixed(1)}%</div>
                </div>
                <div className="result-panel-card">
                  <small>Risk Index</small>
                  <div style={{ fontSize: '1.3rem', fontWeight: 700 }}>{resultVisuals.insightMetrics.riskIndex.toFixed(1)}%</div>
                </div>
                <div className="result-panel-card">
                  <small>Resilience Index</small>
                  <div style={{ fontSize: '1.3rem', fontWeight: 700 }}>{resultVisuals.insightMetrics.resilienceIndex.toFixed(1)}%</div>
                </div>
              </div>

              <div className="row mt-4">
                <div className="col-md-6 mb-3">
                  <div className="result-panel-card">
                    <h5 style={{ color: '#556022', marginBottom: '0.75rem' }}>Modality Stress Graph</h5>
                    <div style={{ width: '100%', height: 260 }}>
                      <ResponsiveContainer>
                        <BarChart data={resultVisuals.modalityBars}>
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(85,96,34,0.2)" />
                          <XAxis dataKey="modality" tick={{ fill: '#556022', fontSize: 12 }} />
                          <YAxis tick={{ fill: '#556022', fontSize: 12 }} />
                          <Tooltip />
                          <Legend />
                          <Bar dataKey="stress" name="Stress %" fill="#c74545" radius={[6, 6, 0, 0]} />
                          <Bar dataKey="calm" name="Calm %" fill="#8d9740" radius={[6, 6, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
                <div className="col-md-6 mb-3">
                  <div className="result-panel-card">
                    <h5 style={{ color: '#556022', marginBottom: '0.75rem' }}>Health Radar</h5>
                    <div style={{ width: '100%', height: 260 }}>
                      <ResponsiveContainer>
                        <RadarChart data={resultVisuals.radarMetrics}>
                          <PolarGrid stroke="rgba(85,96,34,0.3)" />
                          <PolarAngleAxis dataKey="metric" tick={{ fill: '#556022', fontSize: 12 }} />
                          <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#556022', fontSize: 10 }} />
                          <Radar
                            dataKey="value"
                            name="Score"
                            stroke="#8d9740"
                            fill="#b2bb5f"
                            fillOpacity={0.45}
                          />
                          <Tooltip />
                        </RadarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </div>

              {/* Individual Modality Results */}
              {result.individual_predictions && (
                <div className="row mt-4">
                  <div className="col-12">
                    <h5 style={{marginBottom: '1rem', color: '#556022'}}>Individual Modality Analysis</h5>
                    <div style={{display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap'}}>
                      {result.individual_predictions.facial !== null && (
                        <div style={{
                          background: 'rgba(178, 187, 95, 0.2)',
                          padding: '1rem',
                          borderRadius: '8px',
                          minWidth: '150px'
                        }}>
                          <div style={{fontSize: '2rem', marginBottom: '0.5rem'}}>📸</div>
                          <small style={{color: '#556022'}}>Facial</small>
                          <div style={{fontSize: '1.5rem', fontWeight: 'bold'}}>
                            {(result.individual_predictions.facial * 100).toFixed(1)}%
                          </div>
                        </div>
                      )}
                      {result.individual_predictions.voice !== null && (
                        <div style={{
                          background: 'rgba(178, 187, 95, 0.2)',
                          padding: '1rem',
                          borderRadius: '8px',
                          minWidth: '150px'
                        }}>
                          <div style={{fontSize: '2rem', marginBottom: '0.5rem'}}>🎤</div>
                          <small style={{color: '#556022'}}>Voice</small>
                          <div style={{fontSize: '1.5rem', fontWeight: 'bold'}}>
                            {(result.individual_predictions.voice * 100).toFixed(1)}%
                          </div>
                        </div>
                      )}
                      {result.individual_predictions.physiological !== null && (
                        <div style={{
                          background: 'rgba(178, 187, 95, 0.2)',
                          padding: '1rem',
                          borderRadius: '8px',
                          minWidth: '150px'
                        }}>
                          <div style={{fontSize: '2rem', marginBottom: '0.5rem'}}>⚡</div>
                          <small style={{color: '#556022'}}>Physiological</small>
                          <div style={{fontSize: '1.5rem', fontWeight: 'bold'}}>
                            {(result.individual_predictions.physiological * 100).toFixed(1)}%
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              <p style={{
                background: 'rgba(178, 187, 95, 0.1)',
                padding: '1rem',
                borderRadius: '8px',
                marginTop: '1.5rem'
              }}>
                <strong>Recommendation:</strong> {getRecommendation(result.stress_level)}
              </p>

              <div className="result-enhancements" style={{ marginTop: '1.25rem', textAlign: 'left' }}>
                <div className="row" style={{ marginTop: '0.25rem' }}>
                  <div className="col-md-6 mb-4">
                    <AnalysisPanel result={result} />
                  </div>
                  <div className="col-md-6 mb-4">
                    <InsightCards
                      result={result}
                      recoveryScore={recoveryScore}
                      stressLevel={stressLevel}
                    />
                  </div>
                </div>

                <CopilotMessage stressLevel={stressLevel} explainability={result.explainability} />

                <GamePanel
                  stressLevel={stressLevel}
                  isGameActive={isGameActive}
                  setIsGameActive={setIsGameActive}
                  selectedActivity={selectedActivity}
                  setSelectedActivity={setSelectedActivity}
                  onActivityComplete={handleActivityComplete}
                />

                <RewardSystem reward={reward} calmStreak={calmStreak} />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Input Section */}
      <div className="row">
        <div className="col-12">
          <div className="neon-card">
            <h3 className="text-center mb-4">Provide Your Data</h3>
            <p className="text-center" style={{color: '#556022', marginBottom: '2rem'}}>
              Upload any combination of facial images, voice recordings, or physiological data for comprehensive stress analysis
            </p>

            <div className="row">
              {/* Facial Input */}
              <div className="col-md-6 mb-4">
                <div style={{
                  border: '2px dashed rgba(178, 187, 95, 0.3)',
                  borderRadius: '12px',
                  padding: '1.5rem',
                  background: 'rgba(178, 187, 95, 0.05)'
                }}>
                  <div className="text-center mb-3">
                    <span style={{fontSize: '3rem'}}>📸</span>
                    <h4>Facial Analysis</h4>
                    <p style={{color: '#556022', fontSize: '0.9rem'}}>
                      Upload a photo or use webcam
                    </p>
                  </div>

                  {facePreview && (
                    <div style={{marginBottom: '1rem', position: 'relative'}}>
                      <img 
                        src={facePreview} 
                        alt="Preview" 
                        style={{
                          width: '100%',
                          borderRadius: '8px',
                          maxHeight: '200px',
                          objectFit: 'cover'
                        }}
                      />
                      <button
                        onClick={() => {
                          setFaceImage(null);
                          setFacePreview(null);
                        }}
                        className="btn btn-danger"
                        style={{
                          position: 'absolute',
                          top: '8px',
                          right: '8px',
                          padding: '0.25rem 0.5rem',
                          fontSize: '0.875rem'
                        }}
                      >
                        Remove
                      </button>
                    </div>
                  )}

                  {webcamActive && (
                    <div style={{marginBottom: '1rem'}}>
                      <video 
                        ref={videoRef} 
                        autoPlay 
                        style={{width: '100%', borderRadius: '8px'}}
                      />
                      <button
                        onClick={captureWebcam}
                        className="btn btn-neon w-100 mt-2"
                      >
                        📷 Capture Photo
                      </button>
                      <button
                        onClick={analyzeLiveWebcam}
                        className="btn btn-outline-neon w-100 mt-2"
                      >
                        ⚡ Analyze Live Frame
                      </button>
                      <button
                        onClick={stopWebcam}
                        className="btn btn-outline-neon w-100 mt-2"
                      >
                        Cancel
                      </button>

                      {liveFaceResult && (
                        <div className="result-panel-card" style={{ marginTop: '0.75rem' }}>
                          <small>Live Facial Result</small>
                          <div style={{ fontWeight: 700 }}>
                            {liveFaceResult.stress_level || liveFaceResult.predicted_class} ({Number(liveFaceResult.percentage || 0).toFixed(1)}%)
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {!webcamActive && !facePreview && (
                    <>
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleFaceUpload}
                        className="form-control mb-2"
                      />
                      <button
                        onClick={startWebcam}
                        className="btn btn-outline-neon w-100"
                      >
                        📹 Use Webcam
                      </button>
                    </>
                  )}
                  <canvas ref={canvasRef} style={{display: 'none'}} />
                </div>
              </div>

              {/* Voice Input */}
              <div className="col-md-6 mb-4">
                <div style={{
                  border: '2px dashed rgba(178, 187, 95, 0.3)',
                  borderRadius: '12px',
                  padding: '1.5rem',
                  background: 'rgba(178, 187, 95, 0.05)'
                }}>
                  <div className="text-center mb-3">
                    <span style={{fontSize: '3rem'}}>🎤</span>
                    <h4>Voice Analysis</h4>
                    <p style={{color: '#556022', fontSize: '0.9rem'}}>
                      Upload an audio recording
                    </p>
                  </div>

                  {voicePreviewUrl && (
                    <div style={{marginBottom: '1rem'}}>
                      <audio 
                        controls 
                        src={voicePreviewUrl} 
                        style={{width: '100%', marginBottom: '0.5rem'}} 
                      />
                      <button
                        onClick={() => {
                          setVoiceFile(null);
                          setVoicePreviewUrl(null);
                        }}
                        className="btn btn-danger w-100"
                        style={{fontSize: '0.875rem'}}
                      >
                        Remove Audio
                      </button>
                    </div>
                  )}

                  {!voicePreviewUrl && (
                    <>
                      <input
                        type="file"
                        accept="audio/*"
                        onChange={handleVoiceUpload}
                        className="form-control"
                      />
                      <small style={{color: '#556022', display: 'block', marginTop: '0.5rem'}}>
                        Supported: WAV, MP3, OGG, M4A, WEBM
                      </small>

                      <div style={{ display: 'flex', gap: '0.6rem', marginTop: '0.6rem', flexWrap: 'wrap' }}>
                        <button
                          type="button"
                          className="btn btn-neon"
                          onClick={startMicRecording}
                          disabled={isMicRecording}
                        >
                          🎙️ Start Mic
                        </button>
                        <button
                          type="button"
                          className="btn btn-outline-neon"
                          onClick={stopMicRecording}
                          disabled={!isMicRecording}
                        >
                          ⏹️ Stop & Analyze
                        </button>
                      </div>

                      <div style={{ width: '100%', height: 160, marginTop: '0.75rem' }}>
                        <ResponsiveContainer>
                          <AreaChart data={micWaveformData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(85,96,34,0.2)" />
                            <XAxis dataKey="index" hide />
                            <YAxis hide domain={[-1, 1]} />
                            <Tooltip />
                            <Area type="monotone" dataKey="amplitude" stroke="#8d9740" fill="#b2bb5f" fillOpacity={0.35} />
                          </AreaChart>
                        </ResponsiveContainer>
                      </div>

                      {liveVoiceResult && (
                        <div className="result-panel-card" style={{ marginTop: '0.75rem' }}>
                          <small>Live Voice Result</small>
                          <div style={{ fontWeight: 700 }}>
                            {liveVoiceResult.stress_level || liveVoiceResult.predicted_class} ({Number(liveVoiceResult.percentage || 0).toFixed(1)}%)
                          </div>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>

              {/* Physiological Input */}
              <div className="col-12 mb-4">
                <div style={{
                  border: '2px dashed rgba(178, 187, 95, 0.3)',
                  borderRadius: '12px',
                  padding: '1.5rem',
                  background: 'rgba(178, 187, 95, 0.05)'
                }}>
                  <div className="text-center mb-3">
                    <span style={{fontSize: '3rem'}}>🧠⚡</span>
                    <h4>Physiological Data</h4>
                    <p style={{color: '#556022', fontSize: '0.9rem'}}>
                      Enter EEG and GSR data as comma-separated values, or use Muse 2 live stream
                    </p>
                  </div>

                  <div style={{
                    marginBottom: '1.5rem',
                    border: '1px solid rgba(178, 187, 95, 0.4)',
                    borderRadius: '10px',
                    padding: '1rem',
                    background: 'rgba(178, 187, 95, 0.08)'
                  }}>
                    <h5 style={{ marginBottom: '0.75rem' }}>Muse 2 Real-Time Stream</h5>
                    <p style={{ color: '#556022', marginBottom: '0.75rem' }}>
                      Uses muselsl command: python -m muselsl record --duration X --filename C:\\Musedata\\eeg_session.csv
                    </p>

                    <div className="row">
                      <div className="col-md-4 mb-2">
                        <label className="form-label"><strong>Duration (seconds)</strong></label>
                        <input
                          type="number"
                          min="5"
                          max="1800"
                          className="form-control"
                          value={museDuration}
                          onChange={(e) => setMuseDuration(e.target.value)}
                        />
                      </div>
                      <div className="col-md-8 mb-2">
                        <label className="form-label"><strong>CSV output path</strong></label>
                        <input
                          type="text"
                          className="form-control"
                          value={museFilename}
                          onChange={(e) => setMuseFilename(e.target.value)}
                          placeholder="C:\\Musedata\\eeg_session.csv"
                        />
                      </div>
                    </div>

                    <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
                      <button
                        type="button"
                        className="btn btn-neon"
                        disabled={museCollecting}
                        onClick={startMuseCapture}
                      >
                        {museCollecting ? 'Collecting...' : 'Start Muse Stream'}
                      </button>
                      <button
                        type="button"
                        className="btn btn-outline-neon"
                        disabled={!museCollecting}
                        onClick={stopMuseCapture}
                      >
                        Stop Stream
                      </button>
                      <button
                        type="button"
                        className="btn btn-outline-neon"
                        onClick={pollMuseStatus}
                      >
                        Refresh Status
                      </button>
                    </div>

                    <div style={{ marginTop: '0.75rem', color: '#556022' }}>
                      <strong>Status:</strong> {museCollecting ? 'Collecting live data' : 'Idle'} | <strong>Elapsed:</strong> {museElapsed}s
                    </div>

                    {museSessionError && (
                      <div style={{ marginTop: '0.5rem', color: '#c74545' }}>
                        <strong>Error:</strong> {museSessionError}
                      </div>
                    )}

                    <div style={{ width: '100%', height: 280, marginTop: '1rem' }}>
                      <ResponsiveContainer>
                        <LineChart data={musePoints}>
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(85, 96, 34, 0.25)" />
                          <XAxis dataKey="timestamp" tick={{ fill: '#556022', fontSize: 12 }} />
                          <YAxis tick={{ fill: '#556022', fontSize: 12 }} />
                          <Tooltip />
                          <Legend />
                          <Line type="monotone" dataKey="TP9" stroke="#4f772d" dot={false} strokeWidth={2} />
                          <Line type="monotone" dataKey="AF7" stroke="#8d9740" dot={false} strokeWidth={2} />
                          <Line type="monotone" dataKey="AF8" stroke="#bc6c25" dot={false} strokeWidth={2} />
                          <Line type="monotone" dataKey="TP10" stroke="#c74545" dot={false} strokeWidth={2} />
                          <Line type="monotone" dataKey="RightAUX" stroke="#6a4c93" dot={false} strokeWidth={2} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>

                    <small style={{ color: '#556022' }}>
                      Expected columns: timestamps, TP9, AF7, AF8, TP10, Right AUX. Prediction is triggered automatically when recording finishes.
                    </small>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label">
                        <strong>🧠 EEG Data</strong>
                      </label>
                      <textarea
                        value={eegData}
                        onChange={(e) => handleEegTextChange(e.target.value)}
                        placeholder="e.g., 0.5, 0.7, 0.6, 0.8, 0.65, 0.72..."
                        className="form-control"
                        rows="3"
                      />
                      <small style={{color: '#556022'}}>
                        Enter brainwave measurement values
                      </small>
                      <div style={{marginTop: '0.5rem'}}>
                        <input
                          type="file"
                          accept=".csv,.txt"
                          onChange={(e) => handleEegFileUpload(e.target.files[0] || null)}
                          className="form-control"
                        />
                        <small style={{color: '#556022'}}>
                          Optional: upload EEG machine export (CSV/TXT)
                        </small>
                      </div>
                    </div>

                    <div className="col-md-6 mb-3">
                      <label className="form-label">
                        <strong>⚡ GSR Data</strong>
                      </label>
                      <textarea
                        value={gsrData}
                        onChange={(e) => handleGsrTextChange(e.target.value)}
                        placeholder="e.g., 2.1, 2.3, 2.5, 2.4, 2.6, 2.2..."
                        className="form-control"
                        rows="3"
                      />
                      <small style={{color: '#556022'}}>
                        Enter skin conductance values
                      </small>
                      <div style={{marginTop: '0.5rem'}}>
                        <input
                          type="file"
                          accept=".csv,.txt"
                          onChange={(e) => handleGsrFileUpload(e.target.files[0] || null)}
                          className="form-control"
                        />
                        <small style={{color: '#556022'}}>
                          Optional: upload GSR export (CSV/TXT)
                        </small>
                      </div>
                    </div>
                  </div>

                  {(eegPreviewData.length > 0 || gsrPreviewData.length > 0) && (
                    <div className="row mt-2">
                      <div className="col-md-6 mb-3">
                        <div className="result-panel-card">
                          <h5 style={{ color: '#556022', marginBottom: '0.75rem' }}>EEG Preview Chart</h5>
                          <div style={{ width: '100%', height: 220 }}>
                            <ResponsiveContainer>
                              <LineChart data={eegPreviewData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(85,96,34,0.2)" />
                                <XAxis dataKey="index" tick={{ fill: '#556022', fontSize: 11 }} />
                                <YAxis tick={{ fill: '#556022', fontSize: 11 }} />
                                <Tooltip />
                                <Legend />
                                {eegPreviewKeys.map((key, idx) => (
                                  <Line
                                    key={key}
                                    type="monotone"
                                    dataKey={key}
                                    dot={false}
                                    strokeWidth={2}
                                    stroke={["#4f772d", "#8d9740", "#bc6c25", "#c74545", "#6a4c93"][idx % 5]}
                                  />
                                ))}
                              </LineChart>
                            </ResponsiveContainer>
                          </div>
                        </div>
                      </div>

                      <div className="col-md-6 mb-3">
                        <div className="result-panel-card">
                          <h5 style={{ color: '#556022', marginBottom: '0.75rem' }}>GSR Preview Chart</h5>
                          <div style={{ width: '100%', height: 220 }}>
                            <ResponsiveContainer>
                              <LineChart data={gsrPreviewData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(85,96,34,0.2)" />
                                <XAxis dataKey="index" tick={{ fill: '#556022', fontSize: 11 }} />
                                <YAxis tick={{ fill: '#556022', fontSize: 11 }} />
                                <Tooltip />
                                <Legend />
                                {gsrPreviewKeys.map((key, idx) => (
                                  <Line
                                    key={key}
                                    type="monotone"
                                    dataKey={key}
                                    dot={false}
                                    strokeWidth={2}
                                    stroke={["#8d9740", "#4f772d", "#bc6c25"][idx % 3]}
                                  />
                                ))}
                              </LineChart>
                            </ResponsiveContainer>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="text-center mt-4">
              <button
                onClick={analyzeMultimodal}
                disabled={analyzing}
                className="btn btn-neon"
                style={{
                  padding: '0.75rem 3rem',
                  fontSize: '1.1rem',
                  marginRight: '1rem'
                }}
              >
                {analyzing ? '⏳ Analyzing...' : '🔍 Analyze Stress Level'}
              </button>
              <button
                onClick={clearAll}
                className="btn btn-outline-neon"
                style={{
                  padding: '0.75rem 2rem',
                  fontSize: '1.1rem'
                }}
              >
                🗑️ Clear All
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* How to Use Section */}
      <div className="row mt-5">
        <div className="col-12">
          <div className="neon-card">
            <h3 className="text-center mb-4">How to Use the Dashboard</h3>
            <div className="row">
              <div className="col-md-4">
                <h4 style={{color: '#b2bb5f'}}>📸 Facial Data</h4>
                <ul className="list-unstyled">
                  <li>• Upload a clear photo of your face</li>
                  <li>• Or use webcam for live capture</li>
                  <li>• Ensure good lighting</li>
                  <li>• Look directly at camera</li>
                </ul>
              </div>
              <div className="col-md-4">
                <h4 style={{color: '#b2bb5f'}}>🎤 Voice Data</h4>
                <ul className="list-unstyled">
                  <li>• Upload a voice recording</li>
                  <li>• Speak naturally for 3-5 seconds</li>
                  <li>• Minimize background noise</li>
                  <li>• Use standard audio formats</li>
                </ul>
              </div>
              <div className="col-md-4">
                <h4 style={{color: '#b2bb5f'}}>⚡ Physiological Data</h4>
                <ul className="list-unstyled">
                  <li>• Enter comma-separated values</li>
                  <li>• EEG: Brainwave measurements</li>
                  <li>• GSR: Skin conductance values</li>
                  <li>• Use sensor device outputs</li>
                </ul>
              </div>
            </div>
            <div className="alert" style={{
              background: 'rgba(178, 187, 95, 0.1)',
              border: '1px solid rgba(178, 187, 95, 0.3)',
              marginTop: '1.5rem',
              textAlign: 'center'
            }}>
              <strong>💡 Pro Tip:</strong> For best results, provide multiple data sources. 
              The system uses advanced multimodal fusion to combine insights from all available inputs.
            </div>
          </div>
        </div>
      </div>

      <StressChatbot
        stressLevel={stressLevel}
        stressPercentage={result ? result.percentage : null}
      />
    </div>
  );
}