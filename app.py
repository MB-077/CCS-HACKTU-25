import streamlit as st
import numpy as np

# Title and Styling
st.set_page_config(page_title="ML Predictions | AgriSpace", layout="centered")
st.title("🌱 Smart Agriculture Predictions")
st.markdown("<h2 style='text-align: center;'>ML Predictions</h2>", unsafe_allow_html=True)

# State Management
if 'modal_open' not in st.session_state:
    st.session_state.modal_open = False

if 'current_prediction_type' not in st.session_state:
    st.session_state.current_prediction_type = ''

# Open Modal
def open_modal(prediction_type):
    st.session_state.current_prediction_type = prediction_type
    st.session_state.modal_open = True

# Close Modal
def close_modal():
    st.session_state.modal_open = False
    st.session_state.current_prediction_type = ''

# Prediction Function
def handle_predict():
    st.success(f"Predicting {st.session_state.current_prediction_type} with input values!")

# Card Layout
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌾 Crop Recommendation"):
        open_modal('Crop')

with col2:
    if st.button("💧 Fertilizer Recommendation"):
        open_modal('Fertilizer')

with col3:
    if st.button("📈 Yield Prediction"):
        open_modal('Yield')

# Modal-like Input
if st.session_state.modal_open:
    with st.expander(f"Enter {st.session_state.current_prediction_type} Details", expanded=True):
        if st.session_state.current_prediction_type == 'Crop':
            crop_n = st.number_input("Enter Nitrogen (N)", min_value=0.0)
            crop_p = st.number_input("Enter Phosphorous (P)", min_value=0.0)
            crop_k = st.number_input("Enter Potassium (K)", min_value=0.0)
        elif st.session_state.current_prediction_type == 'Fertilizer':
            fertilizer_temp = st.number_input("Enter Temperature (°C)", min_value=0.0)
            fertilizer_humidity = st.number_input("Enter Humidity (%)", min_value=0.0)
            fertilizer_moisture = st.number_input("Enter Moisture (%)", min_value=0.0)
        elif st.session_state.current_prediction_type == 'Yield':
            yield_state = st.text_input("Enter State Name")
            yield_crop = st.text_input("Enter Crop Type")
            yield_area = st.number_input("Enter Area in Hectares", min_value=0.0)

        # Predict Button
        if st.button("Predict"):
            handle_predict()
            close_modal()

    # Close Modal Button
    if st.button("Close"):
        close_modal()
