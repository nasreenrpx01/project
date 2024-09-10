import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Custom CSS for styling the form and prediction box with vibrant colors
st.markdown("""
    <style>
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-image: url('https://spectrum.ieee.org/media-library/image.jpg?id=29665013');
        background-size: cover;
        background-position: center;
    }
    .input-container {
        background: linear-gradient(135deg, #FF69B4, #8A2BE2); /* Vibrant gradient for input box */
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        color: white;
        text-align: center;
    }
    .input-container h2 {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stNumberInput label {
        font-weight: bold;
        font-size: 16px;
        color: #FFFACD; /* Light yellow text for labels */
    }
    .stNumberInput input {
        border-radius: 8px;
        border: 2px solid #FFF; /* White border around inputs */
    }
    .prediction-box {
        background: linear-gradient(135deg, #32CD32, #FFD700); /* Vibrant gradient for prediction box */
        padding: 20px;
        margin-top: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
    }
    .submit-btn {
        background-color: #FF4500; /* Vibrant orange submit button */
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 18px;
        cursor: pointer;
        border-radius: 10px;
    }
    .submit-btn:hover {
        background-color: #FF6347; /* Lighter orange on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Function to take user inputs
def user_input_f():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Add the heading "Input Parameters"
    st.markdown("<h2>Input Parameters</h2>", unsafe_allow_html=True)
    
    DistanceToSolarNoon = st.number_input("Distance to Solar Noon (degrees)", min_value=-1.56, max_value=2.24, value=0.00, step=0.1)
    Temperature = st.number_input("Temperature (°C)", min_value=-2.64, max_value=2.76, value=0.00, step=0.1)
    WindDirection = st.number_input("Wind Direction (degrees)", min_value=-3.57, max_value=2.59, value=0.00, step=0.1)
    WindSpeed = st.number_input("Wind Speed (m/s)", min_value=-2.37, max_value=2.67, value=0.00, step=0.1)
    Humidity = st.number_input("Humidity (%)", min_value=-2.81, max_value=2.09, value=0.00, step=0.1)
    AvgWindSpeed = st.number_input("Average Wind Speed (m/s)", min_value=-1.61, max_value=2.75, value=0.00, step=0.1)
    AvgPressure = st.number_input("Average Pressure (hPa)", min_value=-2.81, max_value=3.19, value=0.00, step=0.1)
    
    # User inputs the sky cover level manually between 0 and 4
    SkyCover = st.number_input("Sky Cover Level (0-4)", min_value=0, max_value=4, value=0, step=1)
    
    # Creating the feature vector
    skycover_data = {
        'sky-cover_0': 1 if SkyCover == 0 else 0,
        'sky-cover_1': 1 if SkyCover == 1 else 0,
        'sky-cover_2': 1 if SkyCover == 2 else 0,
        'sky-cover_3': 1 if SkyCover == 3 else 0,
        'sky-cover_4': 1 if SkyCover == 4 else 0
    }
    
    # Return all data as a dictionary
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

# Flag to track if submit has been clicked
submit = False

# Display input parameters and submit button initially
if 'submit' not in st.session_state:
    st.session_state.submit = False

if not st.session_state.submit:
    # Get user inputs
    data = user_input_f()

    # Submit button to trigger prediction
    if st.button("Submit", key="submit-btn", help="Click to predict energy generation"):
        st.session_state.submit = True  # Update state to hide the form after submission

# Once submit is clicked, the form disappears and prediction box appears
if st.session_state.submit:
    df = pd.DataFrame(data, index=[0])

    # Check if model file exists
    model_file = 'Finalized_model.pkl'
    if os.path.exists(model_file):
        with st.spinner('Making prediction...'):
            try:
                # Load the pre-trained model
                loaded_model = pickle.load(open(model_file, 'rb'))
                prediction = loaded_model.predict(df)
                
                # Convert kilowatts to joules (3600 seconds in an hour)
                energy_in_joules = prediction[0] * 1000 * 3600
                
                # Display the prediction result with vibrant colors
                st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                st.markdown(f"<strong>Predicted Power Generation:</strong> {prediction[0]:.2f} kW")
                st.markdown(f"<strong>Energy Produced:</strong> {energy_in_joules:.2f} J")
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error in prediction: {e}")
    else:
        st.error(f"Model file '{model_file}' not found. Please upload the model.")
