# Solar Power Generation Prediction 🚀☀️  

## Overview  
This project is a Streamlit-based application designed to predict solar power generation based on environmental parameters. Leveraging machine learning, the application provides users with accurate power predictions while maintaining an intuitive and engaging interface.

## Key Features  
- **Interactive Input Form**:  
  - Users can input environmental parameters such as temperature, wind speed, and sky cover.  
  - Parameters are validated and scaled to ensure compatibility with the model.  
- **Accurate Predictions**:  
  - A pre-trained machine learning model estimates solar power generation (kW) and energy production (Joules).  
- **Stylish Interface**:  
  - Custom CSS styling for a visually appealing and user-friendly experience.  
- **Real-Time Feedback**:  
  - Immediate predictions displayed with a breakdown of power and energy units.  

---

## How It Works  
1. **Input Parameters**:  
   The user provides details such as:  
   - **Distance to Solar Noon**  
   - **Temperature**  
   - **Wind Direction and Speed**  
   - **Humidity**  
   - **Average Wind Speed**  
   - **Average Pressure**  
   - **Sky Cover (Categorical Input)**  

2. **Model Prediction**:  
   - The inputs are preprocessed into a suitable format.  
   - A pre-trained machine learning model (`Finalized_model.pkl`) predicts solar power generation in kilowatts.  
   - Energy production in Joules is calculated for an estimated 3-hour duration.  

3. **Output**:  
   - Displays predicted power (kW) and energy (J).  
   - Option to return to the input form for further predictions.  

---

## Deployment  
The application is deployed using **Streamlit**, making it accessible to users in a web-based environment.

To run the project locally:
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/solar-power-prediction.git
   ```
2. Install required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:  
   ```bash
   streamlit run app.py
   ```

---

## Technical Details  
- **Programming Language**: Python  
- **Libraries Used**:  
  - `streamlit` for the user interface  
  - `pandas` for data manipulation  
  - `pickle` for loading the pre-trained model  
  - `scikit-learn` for machine learning  

- **Model**:  
  - The model was trained on a dataset containing environmental variables critical for solar power generation prediction.  
  - Features engineered include one-hot encoding for categorical variables and scaling for numerical variables.  

---

## Visual Design  
The application features:  
- A **background image** to set the theme.  
- Responsive **CSS styling** for improved user experience.  
- Flexible layouts to accommodate various screen sizes.

---

## Future Enhancements  
1. **Additional Features**:  
   - Include support for forecasting over longer time durations.  
   - Add graphs for better visualization of predictions.  
2. **Model Improvement**:  
   - Train with larger datasets for increased accuracy.  
   - Experiment with advanced models like Gradient Boosting or Neural Networks.  
3. **Global Deployment**:  
   - Host the app on Streamlit Cloud or AWS for wider accessibility.  

---

## Results and Accuracy  
- The model achieves high accuracy by using scaled environmental features.  
- Power predictions are within a realistic range, ensuring reliability for end-users.

---

## Contact Information  
We’d love to hear your feedback and collaborate on exciting projects!  
- **Name**: Nasreen Fatima  
- **Email**: [nasreenrpx@gmail.com](mailto:nasreenrpx@gmail.com)  
- **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/nasreen-fatima)  

---

## License  
This project is licensed under the MIT License. For details, see the LICENSE file.  

---

**Try it out and harness the power of the sun with data-driven insights!** 🌞
```

This README reflects your professionalism and passion while being approachable for users. Let me know if you'd like to refine any section further!
