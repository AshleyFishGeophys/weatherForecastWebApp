import streamlit as st
import plotly.express as px
from backend import get_data
from datetime import datetime

# Add title, text inout, slides, selectbox, and subheader
st.title("Weather forecast for the next days")
place = st.text_input("Place: ")
days = st.slider("Forecast days", min_value=1, max_value=5,
                 help="Select the number of days of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))

# Make sure the grammar is correct given the num of days
if days == 1:
    st.subheader(f"{option} for the next {days} day in {place}")
else:
    st.subheader(f"{option} for the next {days} days in {place}")

# If there is no place, doesn't throw error since no place is initially provided
if place:
    # Get temperature/sky data
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [dictionary["main"]["temp"] / 10 for dictionary in filtered_data]
            dates = [dictionary["dt_txt"] for dictionary in filtered_data]
            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            sky_conditions = [dictionary["weather"][0]["main"] for dictionary in filtered_data]
            dates = [dictionary["dt_txt"] for dictionary in filtered_data]
            dates_obj = [datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") for date_str in dates]
            formatted_dates = [date_obj.strftime("%B %d, %Y %I:%M:%S %p") for date_obj in dates_obj]

            images = {"Clear": "images_2/clear.jpg",
                      "Clouds": "images_2/cloud.jpg",
                      "Rain": "images_2/rain.jpg",
                      "Snow": "images_2/snow.jpg"}
            image_paths = [images[condition] for condition in sky_conditions]
            for image, date in zip(image_paths, formatted_dates):
                st.image(image, width=150)
                st.caption(date)

    except KeyError:
        st.write("The place you entered does not exist. Try reentering a valid place name!")

