import streamlit as st
import pandas as pd
import pickle

# Initialize session state for showing prediction or input form
if 'show_prediction' not in st.session_state:
    st.session_state.show_prediction = False
if 'data' not in st.session_state:
    st.session_state.data = None

# Custom CSS for background image and centering the input and prediction boxes
st.markdown("""
    <style>
    body {
        background-image: url('https://wallpapers.com/images/hd/black-and-white-solar-panels-jxkip6hmb8k7l2wx.jpg'); /* Replace with your image URL */
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
    }
    .main-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Full height of the screen */
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.9); /* Slightly transparent background */
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 500px; /* Restrict width of form and prediction box */
        width: 100%;
        margin: 0;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .submit-btn, .back-btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin-top: 10px;
        cursor: pointer;
        border-radius: 5px;
    }
    .submit-btn:hover, .back-btn:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Function to display input form
def show_input_form():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.header("Input Parameters")

    # Create a form to collect user inputs
    with st.form(key='input_form'):
        distance_to_solar_noon = st.number_input("Distance to Solar Noon", min_value=-1.56, max_value=2.24, value=0.0, step=0.1)
        temperature = st.number_input("Temperature", min_value=-2.64, max_value=2.76, value=0.0, step=0.1)
        wind_direction = st.number_input("Wind Direction", min_value=-3.57, max_value=2.59, value=0.0, step=0.1)
        wind_speed = st.number_input("Wind Speed", min_value=-2.37, max_value=2.67, value=0.0, step=0.1)
        humidity = st.number_input("Humidity", min_value=-2.81, max_value=2.09, value=0.0, step=0.1)
        avg_wind_speed = st.number_input("Average Wind Speed", min_value=-1.61, max_value=2.75, value=0.0, step=0.1)
        avg_pressure = st.number_input("Average Pressure", min_value=-2.81, max_value=3.19, value=0.0, step=0.1)

        sky_cover = st.selectbox("Sky Cover Level", [0, 1, 2, 3, 4])

        # Submit button inside the form
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.data = {
                'distance-to-solar-noon': distance_to_solar_noon,
                'temperature': temperature,
                'wind-direction': wind_direction,
                'wind-speed': wind_speed,
                'humidity': humidity,
                'average-wind-speed-(period)': avg_wind_speed,
                'average-pressure-(period)': avg_pressure,
                'sky-cover_0': 1 if sky_cover == 0 else 0,
                'sky-cover_1': 1 if sky_cover == 1 else 0,
                'sky-cover_2': 1 if sky_cover == 2 else 0,
                'sky-cover_3': 1 if sky_cover == 3 else 0,
                'sky-cover_4': 1 if sky_cover == 4 else 0
            }
            # After submitting, show the prediction box
            st.session_state.show_prediction = True

    st.markdown('</div>', unsafe_allow_html=True)

# Function to display the prediction box
def show_prediction_box():
    # Load the pre-trained model
    loaded_model = pickle.load(open('Finalized_model.pkl', 'rb'))

    # Create dataframe with user input
    df = pd.DataFrame(st.session_state.data, index=[0])

    # Make prediction
    prediction = loaded_model.predict(df)
    energy_in_joules = prediction[0] * 1000 * 3600

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.header("Prediction")
    st.write(f"Predicted Power Generation: {prediction[0]:.2f} kW")
    st.write(f"Energy Produced: {energy_in_joules:.2f} Joules")

    # Back button to reset the app state and return to the input form
    if st.button("Back to Input Form", key="back-btn"):
        st.session_state.show_prediction = False
    st.markdown('</div>', unsafe_allow_html=True)

# Main function to manage app state
def main():
    # Check whether to show the input form or the prediction box
    if st.session_state.show_prediction:
        show_prediction_box()
    else:
        show_input_form()

if __name__ == "__main__":
    main()
