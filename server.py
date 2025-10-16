from flask import Flask, jsonify, request
from flask_cors import CORS
from voice import predict_stress_from_file, record_and_predict, load_model, LabelEncoder
import os
import numpy as np
import logging
import librosa
from scipy.io import wavfile

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load model and label encoder
try:
    model = load_model('stress_detection_model.h5')
    label_encoder = LabelEncoder()
    label_encoder.classes_ = np.load('label_encoder_classes.npy', allow_pickle=True)
    logger.info("Model and label encoder loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model or label encoder: {str(e)}")
    raise

# Map raw stress labels to friendly text and percentages
stress_label_map = {
    'non_stress': {'display': 'No Stress', 'percentage': 10},
    'low_stress': {'display': 'Low Stress', 'percentage': 30},
    'moderate_stress': {'display': 'Moderate Stress', 'percentage': 50},
    'high_stress': {'display': 'High Stress', 'percentage': 80}
}

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Welcome to the Voice Stress Detection API. Use /api/voice/record for live recording or /api/voice/upload for file uploads (supports WAV and MP3).'
    })

@app.route('/api/voice/record', methods=['POST'])
def voice_record():
    try:
        duration = request.json.get('duration', 3)
        logger.info(f"Starting voice recording for {duration} seconds")
        stress_level = record_and_predict(duration=duration, model=model, label_encoder=label_encoder)
        if stress_level:
            mapped_label = stress_label_map.get(stress_level, {'display': stress_level, 'percentage': 50})
            logger.info(f"Voice recording analysis successful: {stress_level}")
            return jsonify({
                'status': 'success',
                'stress_level': mapped_label['display'],
                'percentage': mapped_label['percentage']
            })
        else:
            logger.error("Failed to analyze voice recording")
            return jsonify({'status': 'error', 'message': 'Failed to analyze voice recording'}), 500
    except Exception as e:
        logger.error(f"Error in voice_record: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/voice/upload', methods=['POST'])
def voice_upload():
    temp_path = None
    try:
        if 'file' not in request.files:
            logger.error("No file part in request")
            return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400
        file = request.files['file']
        if file.filename == '':
            logger.error("No file selected")
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400
        
        filename = file.filename.lower()
        if not (filename.endswith('.wav') or filename.endswith('.mp3')):
            logger.error(f"Invalid file format: {filename}")
            return jsonify({'status': 'error', 'message': 'File must be WAV or MP3 format'}), 400
        
        temp_path = 'temp_upload.wav'
        temp_input_path = 'temp_input_audio' + os.path.splitext(filename)[1]
        file.save(temp_input_path)
        logger.info(f"Saved uploaded file to {temp_input_path}")

        if filename.endswith('.wav'):
            # Direct copy for WAV
            os.rename(temp_input_path, temp_path)
            logger.info(f"Renamed WAV file to {temp_path}")
        else:
            # Convert MP3 to WAV using librosa
            try:
                y, sr = librosa.load(temp_input_path, sr=None)
                # Normalize audio to ensure compatibility
                y = y / np.max(np.abs(y))  # Scale to [-1, 1]
                # Save as WAV
                wavfile.write(temp_path, sr, (y * 32767).astype(np.int16))
                logger.info(f"Converted MP3 to WAV and saved to {temp_path}")
            except Exception as e:
                logger.error(f"Error converting MP3: {str(e)}")
                return jsonify({'status': 'error', 'message': f'Failed to process MP3 file: {str(e)}'}), 500
            finally:
                if os.path.exists(temp_input_path):
                    os.remove(temp_input_path)
                    logger.info(f"Removed temporary input file {temp_input_path}")

        stress_level = predict_stress_from_file(temp_path, model, label_encoder)
        if stress_level:
            mapped_label = stress_label_map.get(stress_level, {'display': stress_level, 'percentage': 50})
            logger.info(f"File analysis successful: {stress_level}")
            return jsonify({
                'status': 'success',
                'stress_level': mapped_label['display'],
                'percentage': mapped_label['percentage']
            })
        else:
            logger.error("Failed to analyze audio file")
            return jsonify({'status': 'error', 'message': 'Failed to analyze audio file'}), 500
    except Exception as e:
        logger.error(f"Error in voice_upload: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            logger.info(f"Removed temporary file {temp_path}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)