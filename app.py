import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Custom CSS to ensure full-screen background image and preview column is visible
st.markdown("""
    <style>
    html, body {
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Full viewport height */
        width: 100vw; /* Full viewport width */
        background-image: url('https://spectrum.ieee.org/media-library/image.jpg?id=29665013');  /* Example URL */
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: relative;
    }
    .preview-column {
        width: 80%;
        padding: 40px;
        background: rgba(255, 255, 255, 0.8); /* Transparent background */
        border-radius: 10px;
    }
    .custom-text {
        font-size: 16px;
        font-weight: bold;
        margin: 5px 0;
    }
    .prediction-text {
        color: #FF33FF;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    .input-title {
        font-size: 20px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for user input
st.sidebar.header('Input Parameters')

def user_input_f():
    st.sidebar.markdown('<div class="input-title">Enter Environmental Data</div>', unsafe_allow_html=True)
    DistanceToSolarNoon = st.sidebar.number_input("Distance to Solar Noon (degrees)", min_value=-1.56, max_value=2.24, value=0.00, step=0.1)
    Temperature = st.sidebar.number_input("Temperature (°C)", min_value=-2.64, max_value=2.76, value=0.00, step=0.1)
    WindDirection = st.sidebar.number_input("Wind Direction (degrees)", min_value=-3.57, max_value=2.59, value=0.00, step=0.1)
    WindSpeed = st.sidebar.number_input("Wind Speed (m/s)", min_value=-2.37, max_value=2.67, value=0.00, step=0.1)
    Humidity = st.sidebar.number_input("Humidity (%)", min_value=-2.81, max_value=2.09, value=0.00, step=0.1)
    AvgWindSpeed = st.sidebar.number_input("Average Wind Speed (m/s)", min_value=-1.61, max_value=2.75, value=0.00, step=0.1)
    AvgPressure = st.sidebar.number_input("Average Pressure (hPa)", min_value=-2.81, max_value=3.19, value=0.00, step=0.1)
    
    SkyCover = st.sidebar.selectbox("Sky Cover Level", [0, 1, 2, 3, 4])
    
    skycover_data = {
        'sky-cover_0': 1 if SkyCover == 0 else 0,
        'sky-cover_1': 1 if SkyCover == 1 else 0,
        'sky-cover_2': 1 if SkyCover == 2 else 0,
        'sky-cover_3': 1 if SkyCover == 3 else 0,
        'sky-cover_4': 1 if SkyCover == 4 else 0
    }
    
    return {
        'distance-to-solar-noon': DistanceToSolarNoon,
        'temperature': Temperature,
        'wind-direction': WindDirection,
        'wind-speed': WindSpeed,
        'humidity': Humidity,
        'average-wind-speed-(period)': AvgWindSpeed,
        'average-pressure-(period)': AvgPressure,
        **skycover_data
    }

data = user_input_f()
df = pd.DataFrame(data, index=[0])

# Add a div with class 'preview-column' for the content
st.markdown('<div class="preview-column">', unsafe_allow_html=True)

# Display the preview box in the main area
st.markdown("### Preview of Input Parameters")
for key, value in data.items():
    formatted_value = f"{value:.2f}" if isinstance(value, float) else value
    st.markdown(f"<p class='custom-text'><strong>{key.replace('-', ' ').capitalize()}:</strong> {formatted_value}</p>", unsafe_allow_html=True)

# Load the pre-trained model and handle error if file not found
model_file = 'Finalized_model.pkl'
if os.path.exists(model_file):
    with st.spinner('Loading the model...'):
        try:
            loaded_model = pickle.load(open(model_file, 'rb'))
            prediction = loaded_model.predict(df)
            
            # Conversion from kilowatts to joules over 1 hour (3600 seconds)
            energy_in_joules = prediction[0] * 1000 * 3600

            # Display the prediction result in kilowatts
            st.markdown("<hr style='border:1px solid #4CAF50'>", unsafe_allow_html=True)
            st.markdown("### Predicted Power Generation")
            st.markdown(f"<p class='prediction-text'>{prediction[0]:.2f} kW</p>", unsafe_allow_html=True)

            # Display the energy result in joules
            st.markdown("### Energy Produced (in Joules)")
            st.markdown(f"<p class='prediction-text'>{energy_in_joules:.2f} J</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in model prediction: {e}")
else:
    st.error(f"Model file '{model_file}' not found. Please upload the model.")

# Close the preview-column div
st.markdown('</div>', unsafe_allow_html=True)
