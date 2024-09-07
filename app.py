import pandas as pd
import streamlit as st
import xgboost as xgb
import pickle

# Custom CSS to ensure full-screen background image and preview column is visible
st.markdown("""
    <style>
    html, body {
        height: 100%;
        margin: 0;
        padding: ;
        overflow: hidden;
    }
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Full viewport height */
        width: 100vw; /* Full viewport width */
        background-image: url('https://media.istockphoto.com/id/1394023633/photo/businessman-holding-a-bright-light-bulb-concept-of-ideas-for-presenting-new-ideas-great.jpg?s=612x612&w=0&k=20&c=fzn1kyi4tGChEB831rg-MvZYNBuFlmWP84zSHdhvl9U=');  /* Example URL */
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: relative; /* Establishes a stacking context */
    }
   .preview-column {
        width: 80%;
        padding: 70px;
       
    }
    .custom-text {
        font-size: 16px;
        font-weight: bold;
        margin: 5px 0;
    }
    .prediction-text {
        color: #FF33FF;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def user_input_f():
    DistanceToSolarNoon = st.sidebar.number_input("Distance to Solar Noon", min_value=-1.56, max_value=2.24, value=0.00, step=0.1)
    Temperature = st.sidebar.number_input("Temperature", min_value=-2.64, max_value=2.76, value=0.00, step=0.1)
    WindDirection = st.sidebar.number_input("Wind Direction", min_value=-3.57, max_value=2.59, value=0.00, step=0.1)
    WindSpeed = st.sidebar.number_input("Wind Speed", min_value=-2.37, max_value=2.67, value=0.00, step=0.1)
    Humidity = st.sidebar.number_input("Humidity", min_value=-2.81, max_value=2.09, value=0.00, step=0.1)
    AvgWindSpeed = st.sidebar.number_input("Average Wind Speed", min_value=-1.61, max_value=2.75, value=0.00, step=0.1)
    AvgPressure = st.sidebar.number_input("Average Pressure", min_value=-2.81, max_value=3.19, value=0.00, step=0.1)
    
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
# Sidebar for user input
st.sidebar.header('Input Parameters')

data = user_input_f()
df = pd.DataFrame(data, index=[0])

# Add a div with class 'background' for the image
st.markdown('<div class="background"></div>', unsafe_allow_html=True)
# Add a div with class 'preview-column' for the content
st.markdown('<div class="preview-column">', unsafe_allow_html=True)

# Display the preview box in the main area
st.markdown("### Preview of Input Parameters")
for key, value in data.items():
    if isinstance(value, float):
        formatted_value = f"{value:.2f}"
    else:
        formatted_value = value
    st.markdown(f"<p class='custom-text'><strong>{key.replace('-', ' ').capitalize()}:</strong> {formatted_value}</p>", unsafe_allow_html=True)

# Load the pre-trained model
loaded_model = pickle.load(open('Finalized_model.pkl', 'rb'))

# Make predictions using the input data
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

# Close the preview-column div
st.markdown('</div>', unsafe_allow_html=True)

