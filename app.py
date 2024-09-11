import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Custom CSS for vibrant colors and layout
st.markdown("""
    <style>
    .input-container {
        background: linear-gradient(135deg, #FF69B4, #8A2BE2);
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
        color: #FFFACD;
    }
    .stNumberInput input {
        border-radius: 8px;
        border: 2px solid #FFF;
        font-size: 14px;
    }
    .prediction-box {
        background: linear-gradient(135deg, #32CD32, #FFD700);
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
    .submit-btn, .back-btn {
        background-color: #FF4500;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 8px;
        margin-top: 15px;
    }
    .submit-btn:hover, .back-btn:hover {
        background-color: #FF6347;
    }
    .back-btn {
        background-color: #1E90FF;
    }
    .back-btn:hover {
        background-color: #4682B4;
    }
    </style>
""", unsafe_allow_html=True)

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

def main():
    # Initialize session state for visibility control
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    # Wrap UI logic in a single click action to avoid needing multiple clicks
    if st.session_state.submitted:
        show_prediction()  # Call prediction box directly if already submitted
    else:
        show_input_form()

def show_input_form():
    data = user_input_f()
    
    # Submit button to trigger prediction
    if st.button("Submit", key="submit-btn", help="Click to predict energy generation"):
        st.session_state.data = data  # Store data in session state
        st.session_state.submitted = True
        st.experimental_rerun()  # Refresh the page immediately to show prediction box

def show_prediction():
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
                
                # Display the prediction result
                st.markdown(f"<strong>Predicted Power Generation:</strong> {prediction[0]:.2f} kW", unsafe_allow_html=True)
                st.markdown(f"<strong>Energy Produced:</strong> {energy_in_joules:.2f} J", unsafe_allow_html=True)
                
                # Add back button to return to input form
                if st.button("Back", key="back-btn", help="Return to input form"):
                    st.session_state.submitted = False
                    st.experimental_rerun()  # Refresh page to return to input form
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")
    else:
        st.error(f"Model file '{model_file}' not found. Please upload the model.")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
