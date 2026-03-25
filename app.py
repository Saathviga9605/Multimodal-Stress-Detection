# import streamlit as st
# import os
# from PIL import Image
# import numpy as np
# import plotly.graph_objects as go
# from tensorflow.keras.models import load_model as keras_load_model

# # ---------------------------
# # StressDetectionModel Wrapper
# # ---------------------------
# class StressDetectionModel:
#     def __init__(self, img_size=(128, 128)):
#         self.img_size = img_size
#         self.model = None

#     def predict_single_image(self, image_path):
#         """Predict stress/no-stress from a single image using self.model"""
#         if self.model is None:
#             return {"error": "Model not loaded"}

#         try:
#             img = Image.open(image_path).convert('RGB')
#             img = img.resize(self.img_size)
#             img_array = np.array(img) / 255.0
#             img_array = np.expand_dims(img_array, axis=0)

#             pred = self.model.predict(img_array)[0][0]

#             return {
#                 "stress_probability": float(pred),
#                 "no_stress_probability": float(1 - pred),
#                 "predicted_class": "Stress" if pred > 0.5 else "No Stress",
#                 "confidence": float(max(pred, 1 - pred))
#             }

#         except Exception as e:
#             return {"error": str(e)}

# # ---------------------------
# # Streamlit App
# # ---------------------------

# # Page configuration
# st.set_page_config(
#     page_title="Stress Detection Model",
#     page_icon="😊",
#     layout="wide"
# )

# # Initialize session state
# if 'model_loaded' not in st.session_state:
#     st.session_state.model_loaded = False
# if 'model' not in st.session_state:
#     st.session_state.model = None

# @st.cache_resource
# def load_trained_model(model_path):
#     """Load trained Keras model"""
#     if os.path.exists(model_path):
#         model = keras_load_model(model_path)
#         return model
#     else:
#         st.error(f"Model file not found: {model_path}")
#         st.info("Please train the model first by running: python stress_model.py")
#         return None

# # ---------------------------
# # Main app
# # ---------------------------
# def main():
#     st.title("😊 Stress Detection Model")
    
#     page = st.sidebar.selectbox("Choose a page", ["Model Testing", "Model Training", "About"])
    
#     if page == "Model Testing":
#         model_testing_page()
#     elif page == "Model Training":
#         model_training_page()
#     else:
#         about_page()

# # ---------------------------
# # Model Testing Page
# # ---------------------------
# def model_testing_page():
#     st.header("🧠 Model Testing")
    
#     # Load model
#     if not st.session_state.model_loaded:
#         with st.spinner("Loading model..."):
#             model_path = r'E:\Sem 5\SDP_15_oct\ml model\final_stress_detection_model.h5'
#             st.session_state.model = load_trained_model(model_path)
#             if st.session_state.model is not None:
#                 st.session_state.model_loaded = True
#                 st.success("Model loaded successfully!")
#             else:
#                 st.error("Failed to load model.")
#                 return
    
#     uploaded_file = st.file_uploader("Upload an Image", type=['jpg', 'jpeg', 'png'])
    
#     if uploaded_file:
#         image = Image.open(uploaded_file)
#         st.image(image, caption="Uploaded Image", use_column_width=True)
        
#         # Save temporarily
#         temp_path = "temp_image.jpg"
#         image.save(temp_path)
        
#         # Predict using wrapper
#         wrapper_model = StressDetectionModel(img_size=(128,128))
#         wrapper_model.model = st.session_state.model
#         result = wrapper_model.predict_single_image(temp_path)
        
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
        
#         if "error" in result:
#             st.error(result["error"])
#         else:
#             stress_prob = result['stress_probability']
#             no_stress_prob = result['no_stress_probability']
#             predicted_class = result['predicted_class']
#             confidence = result['confidence']
            
#             # Prediction display
#             if predicted_class == "Stress":
#                 st.markdown(f"<h2 style='color:red'>🚨 {predicted_class} Detected</h2>", unsafe_allow_html=True)
#             else:
#                 st.markdown(f"<h2 style='color:green'>😊 {predicted_class} Detected</h2>", unsafe_allow_html=True)
            
#             st.metric("Confidence", f"{confidence:.2%}")
            
#             # Probability bar chart
#             fig = go.Figure(data=[go.Bar(
#                 x=['No Stress', 'Stress'],
#                 y=[no_stress_prob, stress_prob],
#                 marker_color=['#4caf50', '#f44336'],
#                 text=[f'{no_stress_prob:.2%}', f'{stress_prob:.2%}'],
#                 textposition='auto'
#             )])
#             fig.update_layout(title="Stress Detection Probabilities", yaxis=dict(range=[0, 1]))
#             st.plotly_chart(fig, use_container_width=True)

# # ---------------------------
# # Model Training Page
# # ---------------------------
# def model_training_page():
#     st.header("🏋️ Model Training")
#     st.info("Training code runs via stress_model.py. It may take several hours.")
#     if st.button("🚀 Train Model"):
#         st.warning("⚠️ Ensure your dataset is ready and sufficient resources are available.")
#         import subprocess, sys
#         subprocess.run([sys.executable, "stress_model.py"])

# # ---------------------------
# # About Page
# # ---------------------------
# def about_page():
#     st.header("📖 About")
#     st.write("This project detects stress from facial images using a trained deep learning model.")
#     st.write("Upload an image in 'Model Testing' to see predictions.")

# # ---------------------------
# # Run the app
# # ---------------------------
# if __name__ == "__main__":
#     main()

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import json
import csv
import subprocess
import sys
import threading
import time
from io import StringIO
import urllib.request
import urllib.error
from werkzeug.utils import secure_filename
import tempfile
import cv2
import librosa
from model import MultimodalStressDetector

try:
    import shap
    SHAP_AVAILABLE = True
except Exception:
    shap = None
    SHAP_AVAILABLE = False

app = Flask(__name__)
CORS(app)

def get_env_or_dotenv(key, default=''):
    value = os.getenv(key)
    if value:
        return value

    dotenv_path = '.env'
    if not os.path.exists(dotenv_path):
        return default

    try:
        with open(dotenv_path, 'r', encoding='utf-8') as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                if k.strip() == key:
                    return v.strip().strip('"').strip("'")
    except Exception:
        return default

    return default

GEMINI_API_KEY = get_env_or_dotenv('GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a', 'webm'}
ALLOWED_SIGNAL_EXTENSIONS = {'csv', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.errorhandler(413)
def request_entity_too_large(_error):
    return jsonify({
        'status': 'error',
        'message': 'Uploaded file is too large. Maximum allowed size is 50MB.'
    }), 413

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the model
model = MultimodalStressDetector()

# Try to load pre-trained model if it exists
MODEL_PATH = 'multimodal_stress_model.pkl'
if os.path.exists(MODEL_PATH):
    try:
        model.load_model(MODEL_PATH)
        print("Pre-trained model loaded successfully!")
    except Exception as e:
        print(f"Could not load pre-trained model: {e}")
        print("Please train the model first using train_model.py")

MUSE_DEFAULT_FILENAME = r"C:\Musedata\eeg_session.csv"
MUSE_SESSION_LOCK = threading.Lock()
MUSE_SESSION = {
    'process': None,
    'duration_seconds': 0,
    'file_path': MUSE_DEFAULT_FILENAME,
    'started_at': None,
    'completed': False,
    'prediction': None,
    'error': None,
}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def parse_numeric_csv_file(file_storage, signal_type='eeg'):
    """Extract numeric signal values from CSV/TXT, preferring channel columns and skipping timestamp-like fields."""
    try:
        raw_text = file_storage.read().decode('utf-8', errors='ignore')
        file_storage.stream.seek(0)
    except Exception:
        return np.array([])

    rows = list(csv.reader(StringIO(raw_text)))
    if not rows:
        return np.array([])

    first_row = rows[0]

    def _is_numeric(token):
        try:
            float(token)
            return True
        except (ValueError, TypeError):
            return False

    has_header = any(cell and not _is_numeric(cell.strip()) for cell in first_row)
    headers = [cell.strip().lower() for cell in first_row] if has_header else []
    data_rows = rows[1:] if has_header else rows

    if not data_rows:
        return np.array([])

    num_cols = max(len(r) for r in data_rows)
    cols = [[] for _ in range(num_cols)]

    for row in data_rows:
        for idx in range(num_cols):
            token = row[idx].strip() if idx < len(row) else ''
            if not token:
                continue
            try:
                value = float(token)
                if np.isfinite(value):
                    cols[idx].append(value)
            except ValueError:
                continue

    if not any(cols):
        return np.array([])

    keep_col_indices = []
    for idx, values in enumerate(cols):
        if len(values) < 5:
            continue

        header = headers[idx] if idx < len(headers) else ''
        is_timestamp_header = any(word in header for word in ['time', 'timestamp', 'datetime'])
        if is_timestamp_header:
            continue

        arr = np.array(values, dtype=float)
        mostly_increasing = np.mean(np.diff(arr) >= 0) > 0.95 if len(arr) > 10 else False
        looks_like_epoch = np.nanmedian(np.abs(arr)) > 1e6

        # Drop likely timestamp streams when header isn't available.
        if not header and mostly_increasing and looks_like_epoch:
            continue

        keep_col_indices.append(idx)

    if not keep_col_indices:
        # Fallback: flatten everything numeric if we could not infer channels.
        flat = [value for values in cols for value in values]
        return np.array(flat, dtype=float)

    merged = []
    for idx in keep_col_indices:
        merged.extend(cols[idx])

    # Optional light clipping for extreme artifacts in raw streams.
    merged_arr = np.array(merged, dtype=float)
    if signal_type == 'eeg' and merged_arr.size > 0:
        p1, p99 = np.percentile(merged_arr, [1, 99])
        merged_arr = np.clip(merged_arr, p1, p99)

    return merged_arr


def _extract_class1_shap_values(shap_values):
    if isinstance(shap_values, list):
        return np.array(shap_values[1][0], dtype=float)

    arr = np.array(shap_values)
    if arr.ndim == 3:
        # Handles shape like (samples, features, classes)
        return np.array(arr[0, :, 1], dtype=float)
    if arr.ndim == 2:
        return np.array(arr[0], dtype=float)
    return np.array(arr, dtype=float).flatten()


def _extract_class1_expected_value(expected_value):
    if isinstance(expected_value, list):
        return float(expected_value[1])

    arr = np.array(expected_value)
    if arr.ndim == 1 and arr.size >= 2:
        return float(arr[1])
    if arr.ndim == 0:
        return float(arr)
    return float(arr.flatten()[0])


def _modality_shap_explanation(modality_name, estimator, scaler, raw_features, feature_prefix):
    if raw_features is None or estimator is None or scaler is None:
        return None

    x_raw = np.array(raw_features, dtype=float).reshape(1, -1)
    x_scaled = scaler.transform(x_raw)
    stress_prob = float(estimator.predict_proba(x_scaled)[0][1])

    if not SHAP_AVAILABLE:
        return {
            'modality': modality_name,
            'status': 'unavailable',
            'reason': 'SHAP package is not installed in the backend environment.',
            'stress_probability': stress_prob,
            'top_features': [],
        }

    explainer = shap.TreeExplainer(estimator)
    shap_values = explainer.shap_values(x_scaled)
    class1_values = _extract_class1_shap_values(shap_values)
    base_value = _extract_class1_expected_value(explainer.expected_value)

    top_count = min(6, class1_values.shape[0])
    top_indices = np.argsort(np.abs(class1_values))[::-1][:top_count]

    top_features = []
    for idx in top_indices:
        top_features.append({
            'feature': f'{feature_prefix}_{int(idx)}',
            'feature_index': int(idx),
            'feature_value': float(x_raw[0, idx]),
            'shap_value': float(class1_values[idx]),
            'direction': 'increase' if class1_values[idx] >= 0 else 'decrease',
        })

    return {
        'modality': modality_name,
        'status': 'ok',
        'base_value': base_value,
        'stress_probability': stress_prob,
        'top_features': top_features,
    }


def build_explainability_payload(facial_features=None, voice_features=None, phys_features=None):
    modalities = []

    facial_expl = _modality_shap_explanation(
        modality_name='facial',
        estimator=model.facial_model,
        scaler=model.facial_scaler,
        raw_features=facial_features,
        feature_prefix='facial',
    )
    if facial_expl:
        modalities.append(facial_expl)

    voice_expl = _modality_shap_explanation(
        modality_name='voice',
        estimator=model.voice_model,
        scaler=model.voice_scaler,
        raw_features=voice_features,
        feature_prefix='voice',
    )
    if voice_expl:
        modalities.append(voice_expl)

    phys_expl = _modality_shap_explanation(
        modality_name='physiological',
        estimator=model.phys_model,
        scaler=model.phys_scaler,
        raw_features=phys_features,
        feature_prefix='phys',
    )
    if phys_expl:
        modalities.append(phys_expl)

    top_drivers = []
    for modality in modalities:
        for feat in modality.get('top_features', []):
            top_drivers.append({
                'modality': modality['modality'],
                **feat,
            })

    top_drivers = sorted(top_drivers, key=lambda item: abs(item['shap_value']), reverse=True)[:8]

    return {
        'engine': 'shap',
        'available': SHAP_AVAILABLE,
        'modalities': modalities,
        'top_drivers': top_drivers,
        'message': None if SHAP_AVAILABLE else 'Install shap in backend environment to enable SHAP values.',
    }


def _normalize_header(value):
    return (value or '').strip().lower().replace('_', ' ')


def _read_muse_points(file_path, limit=240):
    if not file_path or not os.path.exists(file_path):
        return []

    points = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return []

        header_map = {_normalize_header(h): h for h in reader.fieldnames}
        ts_key = header_map.get('timestamps') or header_map.get('timestamp')
        tp9_key = header_map.get('tp9')
        af7_key = header_map.get('af7')
        af8_key = header_map.get('af8')
        tp10_key = header_map.get('tp10')
        aux_key = header_map.get('right aux') or header_map.get('rightaux') or header_map.get('aux')

        if not all([ts_key, tp9_key, af7_key, af8_key, tp10_key, aux_key]):
            return []

        for row in reader:
            try:
                points.append({
                    'timestamp': float(row[ts_key]),
                    'TP9': float(row[tp9_key]),
                    'AF7': float(row[af7_key]),
                    'AF8': float(row[af8_key]),
                    'TP10': float(row[tp10_key]),
                    'RightAUX': float(row[aux_key]),
                })
            except (ValueError, TypeError, KeyError):
                continue

    if limit and len(points) > limit:
        return points[-limit:]
    return points


def _read_muse_arrays(file_path):
    points = _read_muse_points(file_path, limit=0)
    if not points:
        return np.array([]), np.array([])

    tp9 = np.array([p['TP9'] for p in points], dtype=float)
    af7 = np.array([p['AF7'] for p in points], dtype=float)
    af8 = np.array([p['AF8'] for p in points], dtype=float)
    tp10 = np.array([p['TP10'] for p in points], dtype=float)
    right_aux = np.array([p['RightAUX'] for p in points], dtype=float)

    eeg_array = np.concatenate([tp9, af7, af8, tp10])
    return eeg_array, right_aux


def _predict_from_muse_csv(file_path):
    eeg_array, gsr_array = _read_muse_arrays(file_path)
    if eeg_array.size == 0:
        return {
            'status': 'error',
            'message': 'No valid Muse channel values found in CSV.',
        }

    phys_features = model.extract_physiological_features(eeg_array, gsr_array)
    result = model.predict(phys_features=phys_features)
    if result.get('status') == 'success':
        result['source'] = 'muse_stream'
        result['explainability'] = build_explainability_payload(phys_features=phys_features)
    return result


def _refresh_muse_session_if_needed():
    with MUSE_SESSION_LOCK:
        proc = MUSE_SESSION.get('process')
        if proc is None:
            return

        if proc.poll() is None:
            return

        if MUSE_SESSION.get('completed'):
            return

        file_path = MUSE_SESSION.get('file_path')
        if not file_path or not os.path.exists(file_path):
            MUSE_SESSION['completed'] = True
            MUSE_SESSION['error'] = 'Recording finished but CSV file was not found.'
            return

        try:
            MUSE_SESSION['prediction'] = _predict_from_muse_csv(file_path)
            MUSE_SESSION['completed'] = True
        except Exception as exc:
            MUSE_SESSION['completed'] = True
            MUSE_SESSION['error'] = f'Failed to analyze Muse recording: {exc}'

def local_chat_fallback(user_message, stress_level):
    query = (user_message or '').strip().lower()

    if 'what is stress' in query or (query.startswith('what is') and 'stress' in query):
        return (
            "Stress is your body and mind's response to pressure or challenge. "
            "Short-term stress can improve focus, but prolonged stress may affect sleep, mood, energy, and concentration. "
            "Try: slow breathing, brief movement, hydration, and task prioritization to regulate it."
        )

    if 'symptom' in query or 'sign' in query:
        return (
            "Common stress signs include muscle tension, fast heartbeat, racing thoughts, irritability, shallow breathing, "
            "and poor sleep. If symptoms persist or feel severe, consult a qualified health professional."
        )

    if 'sleep' in query:
        return (
            "For stress-related sleep issues: avoid screens 60 minutes before bed, keep room cool/dark, "
            "and do 2-3 minutes of slow exhale breathing before sleep."
        )

    guidance = {
        'High': "Try this now: 1) inhale for 4s, exhale for 6s for 5 rounds, 2) loosen shoulders/jaw, 3) take a 2-minute screen break.",
        'Moderate': "Try a quick reset: 1) 60 seconds of slow breathing, 2) drink water, 3) switch to one priority task for 10 minutes.",
        'Low': "You are doing well. Maintain momentum with a 1-minute posture check and short breaks every 45-60 minutes.",
    }

    baseline = guidance.get(stress_level, guidance['Moderate'])
    return (
        "I can help with stress support. "
        f"Current stress context: {stress_level}. "
        f"{baseline} You asked: '{user_message}'."
    )

def ask_gemini_stress_assistant(user_message, stress_level, stress_percentage):
    if not GEMINI_API_KEY:
        return local_chat_fallback(user_message, stress_level)

    prompt = (
        "You are a supportive stress-management assistant in a general stress monitoring app. "
        "Give concise, practical, non-medical advice. Do not diagnose. "
        "If user appears in crisis, suggest contacting local emergency services or a mental health professional. "
        f"Current detected stress level: {stress_level}. "
        f"Current detected stress percentage: {stress_percentage}. "
        f"User question: {user_message}"
    )

    payload = {
        'contents': [
            {
                'parts': [
                    {'text': prompt}
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.5,
            'maxOutputTokens': 350
        }
    }

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    req = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            response_data = json.loads(response.read().decode('utf-8'))

        candidates = response_data.get('candidates', [])
        if not candidates:
            return local_chat_fallback(user_message, stress_level)

        parts = candidates[0].get('content', {}).get('parts', [])
        reply = "\n".join(part.get('text', '') for part in parts).strip()
        return reply or local_chat_fallback(user_message, stress_level)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
        return local_chat_fallback(user_message, stress_level)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_trained': model.is_trained
    })

@app.route('/api/multimodal/analyze', methods=['POST'])
def analyze_multimodal():
    """
    Multimodal stress analysis endpoint
    Accepts: image file, audio file, EEG data, GSR data
    """
    try:
        # Initialize feature holders
        facial_features = None
        voice_features = None
        phys_features = None
        eeg_array = None
        gsr_array = None
        
        # Process facial image if provided
        if 'face_image' in request.files:
            face_file = request.files['face_image']
            if face_file and allowed_file(face_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(face_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                face_file.save(filepath)
                
                # Extract facial features
                facial_features = model.extract_facial_features(filepath)
                
                # Clean up
                os.remove(filepath)
        
        # Process voice audio if provided
        if 'voice_audio' in request.files:
            audio_file = request.files['voice_audio']
            if audio_file and allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
                filename = secure_filename(audio_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                audio_file.save(filepath)
                
                # Extract voice features
                voice_features = model.extract_voice_features(filepath)
                
                # Clean up
                os.remove(filepath)
        
        # Process physiological data if provided
        eeg_data = request.form.get('eeg_data')
        gsr_data = request.form.get('gsr_data')

        if 'eeg_file' in request.files:
            eeg_file = request.files['eeg_file']
            if eeg_file and eeg_file.filename:
                if not allowed_file(eeg_file.filename, ALLOWED_SIGNAL_EXTENSIONS):
                    return jsonify({
                        'status': 'error',
                        'message': 'EEG file must be CSV or TXT format'
                    }), 400

                eeg_array = parse_numeric_csv_file(eeg_file, signal_type='eeg')
                if eeg_array.size == 0:
                    return jsonify({
                        'status': 'error',
                        'message': 'No numeric EEG values found in uploaded file'
                    }), 400

        if 'gsr_file' in request.files:
            gsr_file = request.files['gsr_file']
            if gsr_file and gsr_file.filename:
                if not allowed_file(gsr_file.filename, ALLOWED_SIGNAL_EXTENSIONS):
                    return jsonify({
                        'status': 'error',
                        'message': 'GSR file must be CSV or TXT format'
                    }), 400

                gsr_array = parse_numeric_csv_file(gsr_file, signal_type='gsr')
                if gsr_array.size == 0:
                    return jsonify({
                        'status': 'error',
                        'message': 'No numeric GSR values found in uploaded file'
                    }), 400
        
        if eeg_array is None and eeg_data:
            eeg_array = np.fromstring(eeg_data, sep=',')

        if gsr_array is None and gsr_data:
            gsr_array = np.fromstring(gsr_data, sep=',')

        if (eeg_array is not None and eeg_array.size > 0) or (gsr_array is not None and gsr_array.size > 0):
            phys_features = model.extract_physiological_features(eeg_array, gsr_array)
        
        # Check if at least one modality is provided
        if facial_features is None and voice_features is None and phys_features is None:
            return jsonify({
                'status': 'error',
                'message': 'Please provide at least one input (image, audio, or physiological data)'
            }), 400
        
        # Make prediction
        result = model.predict(
            facial_features=facial_features,
            voice_features=voice_features,
            phys_features=phys_features,
            fusion='average'
        )
        
        if 'error' in result:
            return jsonify({
                'status': 'error',
                'message': result['error']
            }), 400

        result['explainability'] = build_explainability_payload(
            facial_features=facial_features,
            voice_features=voice_features,
            phys_features=phys_features,
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/face/upload', methods=['POST'])
def analyze_face():
    """Facial stress analysis endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({
                'status': 'error',
                'message': 'Invalid file type. Please upload an image (PNG, JPG, JPEG)'
            }), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract features and predict
        facial_features = model.extract_facial_features(filepath)
        result = model.predict(facial_features=facial_features)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/voice/upload', methods=['POST'])
def analyze_voice():
    """Voice stress analysis endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
            return jsonify({
                'status': 'error',
                'message': 'Invalid file type. Please upload an audio file (WAV, MP3, OGG, M4A, WEBM)'
            }), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract features and predict
        voice_features = model.extract_voice_features(filepath)
        result = model.predict(voice_features=voice_features)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/voice/record', methods=['POST'])
def record_voice():
    """Voice recording endpoint (simulated)"""
    # This is a placeholder - actual recording would be done client-side
    return jsonify({
        'status': 'error',
        'message': 'Please use the upload feature instead of recording'
    }), 501

@app.route('/api/webcam/capture', methods=['POST'])
def capture_webcam():
    """Webcam capture endpoint"""
    try:
        # Get base64 image data from request
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No image data provided'
            }), 400
        
        import base64
        from io import BytesIO
        from PIL import Image
        
        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Save temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_webcam.jpg')
        image.save(temp_path)
        
        # Extract features and predict
        facial_features = model.extract_facial_features(temp_path)
        result = model.predict(facial_features=facial_features)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/chat/stress', methods=['POST'])
def stress_chat():
    """Stress assistant chat endpoint backed by Gemini API with local fallback."""
    try:
        payload = request.get_json(silent=True) or {}
        message = (payload.get('message') or '').strip()
        stress_level = payload.get('stress_level', 'Moderate')
        stress_percentage = payload.get('stress_percentage', None)

        if not message:
            return jsonify({
                'status': 'error',
                'message': 'Message is required.'
            }), 400

        reply = ask_gemini_stress_assistant(message, stress_level, stress_percentage)

        return jsonify({
            'status': 'success',
            'reply': reply,
            'provider': 'gemini' if GEMINI_API_KEY else 'local-fallback'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/muse/start', methods=['POST'])
def start_muse_stream():
    """Start Muse LSL CSV recording for a fixed duration."""
    payload = request.get_json(silent=True) or {}

    try:
        duration = int(payload.get('duration', 20))
    except (ValueError, TypeError):
        duration = 20

    duration = max(5, min(duration, 1800))
    file_path = (payload.get('filename') or MUSE_DEFAULT_FILENAME).strip()

    if not file_path:
        return jsonify({'status': 'error', 'message': 'filename is required'}), 400

    output_dir = os.path.dirname(file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with MUSE_SESSION_LOCK:
        current_proc = MUSE_SESSION.get('process')
        if current_proc is not None and current_proc.poll() is None:
            return jsonify({
                'status': 'error',
                'message': 'A Muse recording session is already in progress.'
            }), 409

        cmd = [
            sys.executable,
            '-m',
            'muselsl',
            'record',
            '--duration',
            str(duration),
            '--filename',
            file_path,
        ]

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as exc:
            return jsonify({
                'status': 'error',
                'message': f'Could not start muselsl recording: {exc}'
            }), 500

        MUSE_SESSION['process'] = proc
        MUSE_SESSION['duration_seconds'] = duration
        MUSE_SESSION['file_path'] = file_path
        MUSE_SESSION['started_at'] = time.time()
        MUSE_SESSION['completed'] = False
        MUSE_SESSION['prediction'] = None
        MUSE_SESSION['error'] = None

    return jsonify({
        'status': 'success',
        'message': 'Muse recording started',
        'duration_seconds': duration,
        'file_path': file_path,
        'command': f'python -m muselsl record --duration {duration} --filename {file_path}',
    })


@app.route('/api/muse/stop', methods=['POST'])
def stop_muse_stream():
    """Stop active Muse recording session."""
    with MUSE_SESSION_LOCK:
        proc = MUSE_SESSION.get('process')
        if proc is None or proc.poll() is not None:
            return jsonify({'status': 'success', 'message': 'No active Muse recording.'})

        proc.terminate()
        MUSE_SESSION['completed'] = True
        MUSE_SESSION['error'] = 'Recording stopped by user.'

    return jsonify({'status': 'success', 'message': 'Muse recording stopped.'})


@app.route('/api/muse/status', methods=['GET'])
def muse_stream_status():
    """Return live Muse points and final prediction when available."""
    _refresh_muse_session_if_needed()

    try:
        limit = int(request.args.get('limit', 240))
    except (ValueError, TypeError):
        limit = 240

    limit = max(30, min(limit, 2000))

    with MUSE_SESSION_LOCK:
        proc = MUSE_SESSION.get('process')
        collecting = proc is not None and proc.poll() is None
        file_path = MUSE_SESSION.get('file_path')
        started_at = MUSE_SESSION.get('started_at')
        duration_seconds = MUSE_SESSION.get('duration_seconds')
        completed = MUSE_SESSION.get('completed', False)
        prediction = MUSE_SESSION.get('prediction')
        error = MUSE_SESSION.get('error')

    points = _read_muse_points(file_path, limit=limit)
    elapsed_seconds = int(max(0, time.time() - started_at)) if started_at else 0

    return jsonify({
        'status': 'success',
        'collecting': collecting,
        'completed': completed,
        'duration_seconds': duration_seconds,
        'elapsed_seconds': elapsed_seconds,
        'file_path': file_path,
        'points': points,
        'prediction': prediction,
        'error': error,
    })

if __name__ == '__main__':
    print("Starting Multimodal Stress Detection API...")
    print(f"Model trained: {model.is_trained}")
    if not model.is_trained:
        print("\n⚠️  WARNING: Model not trained!")
        print("Please run train_model.py first to train the model.\n")
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)