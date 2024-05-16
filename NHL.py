import streamlit as st
import pandas as pd
import numpy as np

import os
import gdown
from joblib import load
from sklearn.preprocessing import StandardScaler

model = load('nhl_model.joblib')
scaler = load('nhl_scaler.joblib')




def predict(inputs):
    
    # Define the feature names expected by the model
    feature_names = ['Sex', 'Year', 'AgeGroup', 'Ethnicity', 'Race']
    
    # Mapping dictionaries
    sex_map = {'Male': 0, 'Female': 1}
    ethnicity_map = {'Hispanic': 1, 'Non-Hispanic': 0}
    race_map = {'White': 1, 'Black or African American': 0, 'Asian or Pacific Islander': 2}
    agegroup_map = {
                    '1-4 years': 0,
                    '5-9 years': 1,
                    '10-14 years': 2,
                    '15-19 years': 3,
                    '20-24 years': 4,
                    '25-29 years': 5,
                    '30-34 years': 6,
                    '35-39 years': 7,
                    '40-44 years': 8,
                    '45-49 years': 9,
                    '50-54 years': 10,
                    '55-59 years': 11,
                    '60-64 years': 12,
                    '65-69 years': 13,
                    '70-74 years': 14,
                    '75-79 years': 15,
                    '80-84 years': 16,
                    '85+ years': 17
                    }
    
    
    # Apply mappings
    inputs['Sex'] = sex_map[inputs['Sex']]
    inputs['Ethnicity'] = ethnicity_map[inputs['Ethnicity']]
    inputs['Race'] = race_map[inputs['Race']]
    inputs['AgeGroup'] = agegroup_map[inputs['AgeGroup']]
    
    # Assuming the model expects a DataFrame with the same structure as during training
    input_df = pd.DataFrame([inputs], columns=feature_names)

    # Standardize the input data
    input_df_scaled = scaler.transform(input_df)
    
    # Print input data for debugging
    #st.write('Input Data (Standardized):', input_df_scaled)
    
    prediction = model.predict(input_df_scaled)
    return prediction



# Streamlit user interface
st.title('Predictive Analytics for Non-Hodgkin Lymphoma')

# Creating form for input
with st.form(key='prediction_form'):
    sex = st.selectbox('Sex', options=['Male', 'Female'])
    year = st.number_input('Year', min_value=1900, max_value=2999)
    agegroup = st.selectbox('Age Group', options=[
        '1-4 years', '5-9 years', '10-14 years', '15-19 years', '20-24 years', '25-29 years', '30-34 years', '35-39 years', '40-44 years',           '45-49 years', '50-54 years', '55-59 years', '60-64 years', '65-69 years', '70-74 years', '75-79 years', '80-84 years', '85+ years'
    ])
    ethnicity = st.selectbox('Ethnicity', options=['Hispanic', 'Non-Hispanic'])
    race =  st.selectbox('Race', options=['White','Black or African American', 'Asian or Pacific Islander'])
    
    submit_button = st.form_submit_button(label='Predict')

# Processing prediction
if submit_button:
    input_data = {
        'Sex': sex,
        'Year':year,
        'AgeGroup': agegroup, 
        'Ethnicity': ethnicity,
        'Race': race,
               
    }
    # Predict and decode
    y_pred = predict(input_data)  # Ensure predict() returns the appropriate numeric predictions
    #decoded_predictions = decode_predictions(y_pred.flatten())
    # Create a new array for the rounded predictions
    y_predicted_rounded = np.zeros_like(y_pred)

    # Round each column of y_pred separately to different decimal places
    y_predicted_rounded[:, 0] = np.round(y_pred[:, 0], 1)  # Round "Crude Rate" to 1 decimal place
    y_predicted_rounded[:, 1] = np.round(y_pred[:, 1], 6)  # Round "Survival Rate" to 9 decimal places
    st.write('Crude Mortality Rate:', y_predicted_rounded[:,0])
    st.write('Survival Rate:', y_predicted_rounded[:,1])
  