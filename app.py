import streamlit as st
import os
from PIL import Image
import numpy as np
import plotly.graph_objects as go
from tensorflow.keras.models import load_model as keras_load_model

# ---------------------------
# StressDetectionModel Wrapper
# ---------------------------
class StressDetectionModel:
    def __init__(self, img_size=(128, 128)):
        self.img_size = img_size
        self.model = None

    def predict_single_image(self, image_path):
        """Predict stress/no-stress from a single image using self.model"""
        if self.model is None:
            return {"error": "Model not loaded"}

        try:
            img = Image.open(image_path).convert('RGB')
            img = img.resize(self.img_size)
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            pred = self.model.predict(img_array)[0][0]

            return {
                "stress_probability": float(pred),
                "no_stress_probability": float(1 - pred),
                "predicted_class": "Stress" if pred > 0.5 else "No Stress",
                "confidence": float(max(pred, 1 - pred))
            }

        except Exception as e:
            return {"error": str(e)}

# ---------------------------
# Streamlit App
# ---------------------------

# Page configuration
st.set_page_config(
    page_title="Stress Detection Model",
    page_icon="😊",
    layout="wide"
)

# Initialize session state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'model' not in st.session_state:
    st.session_state.model = None

@st.cache_resource
def load_trained_model(model_path):
    """Load trained Keras model"""
    if os.path.exists(model_path):
        model = keras_load_model(model_path)
        return model
    else:
        st.error(f"Model file not found: {model_path}")
        st.info("Please train the model first by running: python stress_model.py")
        return None

# ---------------------------
# Main app
# ---------------------------
def main():
    st.title("😊 Stress Detection Model")
    
    page = st.sidebar.selectbox("Choose a page", ["Model Testing", "Model Training", "About"])
    
    if page == "Model Testing":
        model_testing_page()
    elif page == "Model Training":
        model_training_page()
    else:
        about_page()

# ---------------------------
# Model Testing Page
# ---------------------------
def model_testing_page():
    st.header("🧠 Model Testing")
    
    # Load model
    if not st.session_state.model_loaded:
        with st.spinner("Loading model..."):
            model_path = r'E:\Sem 5\SDP_15_oct\ml model\final_stress_detection_model.h5'
            st.session_state.model = load_trained_model(model_path)
            if st.session_state.model is not None:
                st.session_state.model_loaded = True
                st.success("Model loaded successfully!")
            else:
                st.error("Failed to load model.")
                return
    
    uploaded_file = st.file_uploader("Upload an Image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Save temporarily
        temp_path = "temp_image.jpg"
        image.save(temp_path)
        
        # Predict using wrapper
        wrapper_model = StressDetectionModel(img_size=(128,128))
        wrapper_model.model = st.session_state.model
        result = wrapper_model.predict_single_image(temp_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if "error" in result:
            st.error(result["error"])
        else:
            stress_prob = result['stress_probability']
            no_stress_prob = result['no_stress_probability']
            predicted_class = result['predicted_class']
            confidence = result['confidence']
            
            # Prediction display
            if predicted_class == "Stress":
                st.markdown(f"<h2 style='color:red'>🚨 {predicted_class} Detected</h2>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 style='color:green'>😊 {predicted_class} Detected</h2>", unsafe_allow_html=True)
            
            st.metric("Confidence", f"{confidence:.2%}")
            
            # Probability bar chart
            fig = go.Figure(data=[go.Bar(
                x=['No Stress', 'Stress'],
                y=[no_stress_prob, stress_prob],
                marker_color=['#4caf50', '#f44336'],
                text=[f'{no_stress_prob:.2%}', f'{stress_prob:.2%}'],
                textposition='auto'
            )])
            fig.update_layout(title="Stress Detection Probabilities", yaxis=dict(range=[0, 1]))
            st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Model Training Page
# ---------------------------
def model_training_page():
    st.header("🏋️ Model Training")
    st.info("Training code runs via stress_model.py. It may take several hours.")
    if st.button("🚀 Train Model"):
        st.warning("⚠️ Ensure your dataset is ready and sufficient resources are available.")
        import subprocess, sys
        subprocess.run([sys.executable, "stress_model.py"])

# ---------------------------
# About Page
# ---------------------------
def about_page():
    st.header("📖 About")
    st.write("This project detects stress from facial images using a trained deep learning model.")
    st.write("Upload an image in 'Model Testing' to see predictions.")

# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    main()
