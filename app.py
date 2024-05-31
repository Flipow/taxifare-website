import streamlit as st
import requests
import datetime
import pandas as pd

# '''
# # TaxiFareModel front
# '''

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

# Date and time input
date = st.date_input("Date of the ride", datetime.date.today())
time = st.time_input("Time of the ride", datetime.datetime.now().time())

# Coordinate inputs
pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)

# Passenger count input
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1)

# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

url = 'https://taxifare.lewagon.ai/predict'

if st.button("Get Fare Prediction"):
    # Combine date and time into a single datetime object
    pickup_datetime = datetime.datetime.combine(date, time)

    # Format datetime as required by the API (ISO 8601 format)
    pickup_datetime_str = pickup_datetime.isoformat()

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# '''

    params = {
        "pickup_datetime": pickup_datetime_str,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    def get_map_data():
        return pd.DataFrame(
            data = {
                'lat': [pickup_latitude, dropoff_latitude],
                'lon': [pickup_longitude, dropoff_longitude]
            }
        )
    df = get_map_data()
    st.map(df)

# 3. Let's call our API using the `requests` package...

    response = requests.get(url, params=params)

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

    if response.status_code == 200:
        prediction = response.json()
        fare = prediction.get("fare", "Error: no fare returned")
        st.write(f"The predicted fare is: ${fare:.2f}")
    else:
        st.write("Error: Unable to get the prediction from the API")
        st.write(f"Response code: {response.status_code}")
        st.write(f"Response content: {response.content}")

## Finally, we can display the prediction to the user
# '''
