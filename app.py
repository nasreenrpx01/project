import streamlit as st
import pandas as pd
import pickle

# Initialize session state for showing prediction or input form
if 'show_prediction' not in st.session_state:
    st.session_state.show_prediction = False
if 'data' not in st.session_state:
    st.session_state.data = None

# Function to display input form
def show_input_form():
    st.header("Input Parameters")
    
    with st.form("input_form"):
        # Create input fields
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

        # If the form is submitted, save data and switch to prediction mode
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
            st.session_state.show_prediction = True

# Function to display the prediction box
def show_prediction_box():
    # Load the pre-trained model
    loaded_model = pickle.load(open('Finalized_model.pkl', 'rb'))

    # Create dataframe with user input
    df = pd.DataFrame(st.session_state.data, index=[0])

    # Make prediction
    prediction = loaded_model.predict(df)
    energy_in_joules = prediction[0] * 1000 * 3600

    st.header("Prediction")
    st.write(f"Predicted Power Generation: {prediction[0]:.2f} kW")
    st.write(f"Energy Produced: {energy_in_joules:.2f} Joules")

    # Back button to reset the app state
    if st.button("Back to Input Form"):
        st.session_state.show_prediction = False

# Main function to manage app state
def main():
    # Check whether to show the input form or the prediction box
    if st.session_state.show_prediction:
        show_prediction_box()
    else:
        show_input_form()

if __name__ == "__main__":
    main()

