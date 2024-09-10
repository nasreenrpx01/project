import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Custom CSS for vibrant colors and layout
st.markdown("""
    <style>
    .input-container {
        background: linear-gradient(135deg, #FF69B4, #8A2BE2); /* Vibrant gradient for input box */
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        color: white;
        text-align: center;
        width: 100%;
        max-width: 500px;
        margin: auto;
    }
    .input-container h2 {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .stNumberInput label {
        font-weight: bold;
        font-size: 14px;
        color: #FFFACD; /* Light yellow text for labels */
    }
    .stNumberInput input {
        border-radius: 8px;
        border: 2px solid #FFF; /* White border around inputs */
        font-size: 14px;
    }
    .prediction-box {
        background: linear-gradient(135deg, #32CD32, #FFD700); /* Vibrant gradient for prediction box */
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);
        width: 100%;
        max-width: 500px;
        margin: auto;
    }
    .submit-btn {
        background-color: #FF4500; /* Vibrant orange submit button */
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 8px;
        margin-top: 15px;
    }
    .submit-btn:hover {
        background-color: #FF6347; /* Lighter orange on hover */
    }
    .hidden {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Function to take user inputs
def user_input_f():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    st.markdown("<h2>Input Parameters</h2>", unsafe_allow_html=True)
    
    DistanceToSolarNoon = st.number_input("Distance to Solar Noon (degrees)", min_value=-1.56, max_value=2.24, value=0.00, step=0.1)
    Temperature = st.number_input("Temperature (°C)", min_value=-2.64, max_value=2.76, value=0.00, step=0.1)
    WindDirection = st.number_input("Wind Direction (degrees)", min_value=-3.57, max_value=2.59, value=0.00, step=0.1)
    WindSpeed = st.number_input("Wind Speed (m/s)", min_value=-2.37, max_value=2.67, value=0.00, step=0.1)
    Humidity = st.number_input("Humidity (%)", min_value=-2.81, max_value=2.09, value=0.00, step=0.1)
    AvgWindSpeed = st.number_input("Average Wind Speed (m/s)", min_value=-1.61, max_value=2.75, value=0.00, step=0.1)
    AvgPressure = st.number_input("Average Pressure (hPa)", min_value=-2.81, max_value=3.19, value=0.00, step=0.1)
    
    SkyCover = st.number_input("Sky Cover Level (0-4)", min_value=0, max_value=4, value=0, step=1)
    
    skycover_data = {
        'sky-cover_0': 1 if SkyCover == 0 else 0,
        'sky-cover_1': 1 if SkyCover == 1 else 0,
        'sky-cover_2': 1 if SkyCover == 2 else 0,
        'sky-cover_3': 1 if SkyCover == 3 else 0,
        'sky-cover_4': 1 if SkyCover == 4 else 0
    }
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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

# Main app logic
def main():
    # Initialize the submit state
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    if not st.session_state.submitted:
        # Display input form
        data = user_input_f()
        
        # Submit button to trigger prediction
        if st.button("Submit", key="submit-btn", help="Click to predict energy generation"):
            st.session_state.data = data  # Store data in session state
            st.session_state.submitted = True  # Set state to hide the form and show predictions

    if st.session_state.submitted:
        # Hide the input form
        st.markdown('<div class="hidden">', unsafe_allow_html=True)
        st.markdown('<div class="hidden">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display prediction results
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        
        # Create DataFrame from the stored data
        df = pd.DataFrame(st.session_state.data, index=[0])

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
                    st.markdown(f"<strong>Predicted Power Generation:</strong> {prediction[0]:.2f} kW", unsafe_allow_html=True)
                    st.markdown(f"<strong>Energy Produced:</strong> {energy_in_joules:.2f} J", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error in prediction: {e}")
        else:
            st.error(f"Model file '{model_file}' not found. Please upload the model.")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
