import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://localhost:8001/predict"

st.title("🦪 Abalone Age Prediction")

st.write("Enter the abalone's physical measurements:")

# Input fields
col1, col2 = st.columns(2)

with col1:
    sex = st.selectbox("Sex", ["M", "F", "I"])
    length = st.number_input("Length (mm)", min_value=0.0, value=0.5, step=0.01)
    diameter = st.number_input("Diameter (mm)", min_value=0.0, value=0.4, step=0.01)
    height = st.number_input("Height (mm)", min_value=0.0, value=0.15, step=0.01)

with col2:
    whole_weight = st.number_input("Whole weight (g)", min_value=0.0, value=0.8, step=0.01)
    shucked_weight = st.number_input("Shucked weight (g)", min_value=0.0, value=0.3, step=0.01)
    viscera_weight = st.number_input("Viscera weight (g)", min_value=0.0, value=0.2, step=0.01)
    shell_weight = st.number_input("Shell weight (g)", min_value=0.0, value=0.2, step=0.01)

# Predict button
if st.button("Predict Age", type="primary"):
    # Prepare payload
    payload = {
        "Sex": sex,
        "Length": length,
        "Diameter": diameter,
        "Height": height,
        "Whole weight": whole_weight,
        "Shucked weight": shucked_weight,
        "Viscera weight": viscera_weight,
        "Shell weight": shell_weight
    }
    
    try:
        # Make request to FastAPI
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 201:
            result = response.json()
            predicted_age = result["predicted_age"]
            
            # Display result
            st.success(f"### Predicted Age: {predicted_age:.2f} years")
        else:
            st.error(f"Error: {response.text}")
    
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")