import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import pydeck as pdk

#title
st.title('TaxiFare Model Front')
#description
st.markdown('''
This app allows you to get a fare prediction for a taxi ride in NYC 🚕.  
Please input the details of the ride below: 👇''')

# Input fields for ride parameters
pickup_date = st.date_input("Pickup date", value=datetime.today())
pickup_time = st.time_input("Pickup time", value=datetime.now().time())
pickup_datetime = f"{pickup_date} {pickup_time}"

pickup_longitude = st.number_input("Pickup longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff latitude", value=40.748817)
passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, value=1)




# DataFrame with pickup and dropoff locations
map_data = pd.DataFrame({
    'lat': [pickup_latitude, dropoff_latitude],
    'lon': [pickup_longitude, dropoff_longitude],
    'label': ['Pickup', 'Dropoff']
})



# Display the basic map
st.subheader("Pickup & Dropoff Locations")
st.map(map_data)






url = 'https://taxifare.lewagon.ai/predict'

# When the button is clicked
if st.button('Get Fare Prediction'):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            prediction = response.json().get("fare", "No fare key in response")
            st.success(f"Predicted fare: ${prediction:.2f}")
        else:
            st.error(f"API Error: {response.status_code}")
    except Exception as e:
        st.error(f"Request failed: {e}")