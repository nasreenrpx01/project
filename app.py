import streamlit as st
import pandas as pd
import pickle

# Initialize session state
if 'show_prediction' not in st.session_state:
    st.session_state.show_prediction = False
if 'data' not in st.session_state:
    st.session_state.data = None

# Custom CSS for background image and centering
st.markdown("""
    <style>
    .main {
        position: relative;
        background-image: url('https://i.pinimg.com/originals/74/91/44/749144aead3fd6ed4bc7892b1bad8498.jpg');
        background-size: cover;
    }
    .content {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        width: 100%;
    }
    .main-container {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        box-sizing: border-box;
        color: white;
    }
    .input-form-container {
        margin-top: 50px; /* Space above the input form */
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



def show_input_form():
    st.markdown('<div class="main"><div class="content"><div class="main-container">', unsafe_allow_html=True)
    st.header("Input Parameters")

    with st.form(key='input_form'):
        distance_to_solar_noon = st.number_input("Distance to Solar Noon", min_value=-1.56, max_value=2.24, value=0.0, step=0.1)
        temperature = st.number_input("Temperature", min_value=-2.64, max_value=2.76, value=0.0, step=0.1)
        wind_direction = st.number_input("Wind Direction", min_value=-3.57, max_value=2.59, value=0.0, step=0.1)
        wind_speed = st.number_input("Wind Speed", min_value=-2.37, max_value=2.67, value=0.0, step=0.1)
        humidity = st.number_input("Humidity", min_value=-2.81, max_value=2.09, value=0.0, step=0.1)
        avg_wind_speed = st.number_input("Average Wind Speed", min_value=-1.61, max_value=2.75, value=0.0, step=0.1)
        avg_pressure = st.number_input("Average Pressure", min_value=-2.81, max_value=3.19, value=0.0, step=0.1)
        sky_cover = st.selectbox("Sky Cover Level", [0, 1, 2, 3, 4])

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
            st.session_state.show_prediction = True

    st.markdown('</div></div></div></div>', unsafe_allow_html=True)

def show_prediction_box():
    loaded_model = pickle.load(open('Finalized_model.pkl', 'rb'))
    df = pd.DataFrame(st.session_state.data, index=[0])
    prediction = loaded_model.predict(df)
    energy_in_joules = prediction[0] * 1000 * 3600

    st.markdown('<div class="main"><div class="content"><div class="main-container">', unsafe_allow_html=True)
    st.header("Estimated Power Generated in 3 hours")
    st.write(f"Predicted Power Generation: {prediction[0]:.2f} kW")
    st.write(f"Prediced Energy Produced: {energy_in_joules:.2f} Joules")

    if st.button("Back to Input Form", key="back-btn"):
        st.session_state.show_prediction = False

    st.markdown('</div></div></div></div>', unsafe_allow_html=True)

def main():
    if st.session_state.show_prediction:
        show_prediction_box()
    else:
        show_input_form()

if __name__ == "__main__":
    main()
