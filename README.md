# Multimodal Stress Detection Platform

An end-to-end stress detection platform that combines multiple biometric and behavioral inputs into one unified stress assessment.

The system includes:

1. A Flask backend for model inference, explainability, Muse capture orchestration, and AI stress-support chat.
2. A React frontend with multimodal input tools, live previews, result analytics, and intervention experiences.
3. A multimodal ML pipeline that fuses facial, voice, and physiological (EEG/GSR) predictions.

## What This Project Supports

## Modalities

1. Facial input
2. Voice input
3. Physiological input (EEG and GSR)
4. Muse 2 real-time EEG stream (CSV capture + live chart + auto-prediction)

## Input methods

1. File upload (image, audio, CSV/TXT signals)
2. Live webcam frame capture and live webcam frame inference
3. Microphone recording in browser with waveform visualization
4. Manual EEG/GSR numeric input as comma-separated values

## Output and interpretation

1. Final stress probability and no-stress probability
2. Stress class and stress level band (Low, Moderate, High)
3. Per-modality stress probabilities
4. Confidence score and percentage summary
5. SHAP explainability payload (global top drivers + per-modality top features)

## Wellness and support features

1. AI stress support chatbot
2. Local fallback chatbot behavior if Gemini key is not configured
3. Interactive recovery activities (breathing, focus tap, calm timer, gratitude, posture reset)
4. Recovery score, calm streak, and reward feedback UI

## Frontend Features (Dashboard)

The dashboard combines collection, analysis, and post-analysis support in one flow.

## Data collection features

1. Facial photo upload preview
2. Webcam start, stop, capture, and instant live frame analysis
3. Voice file upload preview
4. Browser microphone capture with real-time waveform chart
5. EEG text input and CSV/TXT upload with preview chart
6. GSR text input and CSV/TXT upload with preview chart
7. Muse session controls (start, stop, refresh status)

## Result and insight features

1. Main stress score card with probability metrics
2. Modality stress graph (stress vs calm bars)
3. Health radar (risk, agreement, coverage, resilience)
4. Individual modality cards (facial, voice, physiological)
5. Analysis panel with contribution breakdown
6. Insight cards (recovery score, confidence score, trigger summary)
7. Copilot insight bubble with interpreted SHAP drivers

## Recovery and intervention features

1. Guided breathing exercise
2. Focus tap game
3. Calm mode (2-minute timer + optional calming audio)
4. Gratitude reflection mini-game
5. Posture reset checklist
6. Reward and streak feedback after activity completion

## AI Chat Assistant

The chatbot runs through `/api/chat/stress` and supports:

1. Stress-aware prompts using current stress level and percentage
2. Gemini model responses when `GEMINI_API_KEY` is configured
3. Local fallback response engine when Gemini is unavailable

Default Gemini model:

`gemini-2.5-flash`

## Backend API

Base URL (development):

`http://127.0.0.1:5000`

## Core endpoints

1. `GET /api/health`
2. `POST /api/multimodal/analyze`
3. `POST /api/face/upload`
4. `POST /api/voice/upload`
5. `POST /api/voice/record` (placeholder; returns not implemented)
6. `POST /api/webcam/capture`
7. `POST /api/chat/stress`
8. `POST /api/muse/start`
9. `POST /api/muse/stop`
10. `GET /api/muse/status`

## Multimodal analyze request

`POST /api/multimodal/analyze` supports any combination of:

1. `face_image` (image file)
2. `voice_audio` (audio file)
3. `eeg_data` (comma-separated numeric text)
4. `gsr_data` (comma-separated numeric text)
5. `eeg_file` (CSV/TXT)
6. `gsr_file` (CSV/TXT)

At least one valid modality is required.

## Example cURL

```bash
curl -X POST http://127.0.0.1:5000/api/multimodal/analyze \
  -F "face_image=@photo.jpg" \
  -F "voice_audio=@sample.wav" \
  -F "eeg_data=0.52,0.61,0.58,0.64" \
  -F "gsr_data=2.1,2.3,2.2,2.4"
```

## Muse workflow

1. Frontend calls `/api/muse/start` with duration and output filename.
2. Backend launches:

```bash
python -m muselsl record --duration <seconds> --filename <csv-path>
```

3. Frontend polls `/api/muse/status` for live points.
4. On completion, backend auto-runs prediction from the generated CSV.
5. Final prediction (with explainability) is returned in Muse status payload.

## Explainability

Explainability is generated in backend responses under `explainability` and includes:

1. Engine metadata (`shap`)
2. Availability flag
3. Modality-level SHAP summaries
4. Cross-modality `top_drivers`
5. Optional message when SHAP package is not installed

## ML Pipeline (Current Implementation)

The `MultimodalStressDetector` currently uses:

1. One RandomForest classifier per modality
2. One StandardScaler per modality
3. Probability-level fusion by average across available modalities

## Current extraction dimensionality

1. Facial features: 84
2. Voice features: 140
3. Physiological features: 132 (EEG + GSR blocks)

## Training scripts

1. `train_model.py`: trains from prepared dataset files or generates a demo synthetic model
2. `train.py` and `stress_model.py`: additional training/legacy experiments in repository

## Quick Start

## 1) Backend setup

From project root:

```bash
cd stress-detection
python -m venv .venv
```

Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install flask flask-cors numpy pandas scikit-learn imbalanced-learn opencv-python librosa soundfile scipy shap muselsl pillow
```

Train or prepare model:

```bash
python train_model.py
```

Start backend:

```bash
python app.py
```

## 2) Frontend setup

In a new terminal:

```bash
cd stress-detection
npm install
npm start
```

Frontend runs on:

`http://localhost:3000`

The React app uses a development proxy to backend:

`http://127.0.0.1:5000`

## Environment Variables

Optional backend variables:

1. `GEMINI_API_KEY` for chatbot model responses
2. `GEMINI_MODEL` to override default model (`gemini-2.5-flash`)

You can place these in your shell environment or `.env` file in backend working directory.

## File Types and Limits

## Accepted file types

1. Images: `png`, `jpg`, `jpeg`
2. Audio: `wav`, `mp3`, `ogg`, `m4a`, `webm`
3. Signal files: `csv`, `txt`

## Upload limit

Maximum request/file size is configured to 50 MB.

## Muse 2 Notes

To use Muse capture:

1. Ensure `muselsl` is installed in backend environment.
2. Ensure Muse device stream is available to `muselsl`.
3. Ensure output path is writable (default in UI: `C:\Musedata\eeg_session.csv`).

Expected Muse CSV channel headers include:

1. `timestamps` (or `timestamp`)
2. `TP9`
3. `AF7`
4. `AF8`
5. `TP10`
6. `Right AUX` / `RightAUX` / `AUX`

## Project Structure (High Level)

```text
stress-detection/
  app.py
  model.py
  train_model.py
  server.py
  src/
    App.js
    pages/
      Dashboard.js
      Landing.js
      About.js
      Features.js
      Impact.js
    components/
      AnalysisPanel.jsx
      InsightCards.jsx
      CopilotMessage.jsx
      GamePanel.jsx
      RewardSystem.jsx
      BreathingExercise.jsx
      StressChatbot.jsx
  Feature Extraction/
  Dataset/
  uploads/
```

## Important Notes

1. `app.py` is the active multimodal backend used by dashboard API proxy.
2. `server.py` is a legacy backend with older voice/face routes and different model stack.
3. If `multimodal_stress_model.pkl` is missing or incompatible, run `train_model.py` again.
4. `requirements.txt` at workspace root may not list all active backend dependencies; install packages shown in this README for a clean setup.

## Troubleshooting

## Backend says model not trained

1. Run `python train_model.py`
2. Confirm `multimodal_stress_model.pkl` exists in project root
3. Restart backend

## Frontend cannot call backend

1. Confirm backend is running on `127.0.0.1:5000`
2. Confirm frontend is running from same project and proxy is active
3. Check browser/network console for endpoint errors

## SHAP not available in response

1. Install `shap` in backend environment
2. Restart backend

## Muse status shows no data

1. Confirm Muse recording actually wrote CSV to configured path
2. Confirm expected channel headers are present
3. Use Refresh Status after recording completes

## Disclaimer

This system is intended for educational/research and wellness-support contexts. It does not provide medical diagnosis. For persistent or severe symptoms, consult a qualified healthcare professional.

## Contributors

1. Saathviga B
2. Kaviya R