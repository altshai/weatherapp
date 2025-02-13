import streamlit as st
import requests
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# Function to get current weather data
def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

# Function to get historical weather data
def get_historical_weather(lat, lon, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/onecall/timemachine"
    timestamps = [int((datetime.utcnow() - timedelta(hours=i)).timestamp()) for i in range(1, 25)]
    historical_data = []
    
    for timestamp in timestamps:
        params = {
            'lat': lat,
            'lon': lon,
            'dt': timestamp,
            'appid': api_key,
            'units': 'metric'
        }
        response = requests.get(base_url, params=params)
        historical_data.append(response.json())
    
    return historical_data

# Function to plot historical data
def plot_historical_data(historical_data, city):
    hours = [datetime.utcfromtimestamp(data['current']['dt']).strftime('%H:%M') for data in historical_data]
    temperatures = [data['current']['temp'] for data in historical_data]
    humidities = [data['current']['humidity'] for data in historical_data]
    wind_speeds = [data['current']['wind_speed'] for data in historical_data]

    fig, ax = plt.subplots(3, 1, figsize=(10, 15))
    
    ax[0].plot(hours, temperatures, marker='o')
    ax[0].set_title(f'Temperature (°C) in {city} (Past 24 Hours)')
    ax[0].set_xlabel('Time (UTC)')
    ax[0].set_ylabel('Temperature (°C)')
    ax[0].grid(True)

    ax[1].plot(hours, humidities, marker='o', color='orange')
    ax[1].set_title(f'Humidity (%) in {city} (Past 24 Hours)')
    ax[1].set_xlabel('Time (UTC)')
    ax[1].set_ylabel('Humidity (%)')
    ax[1].grid(True)

    ax[2].plot(hours, wind_speeds, marker='o', color='green')
    ax[2].set_title(f'Wind Speed (m/s) in {city} (Past 24 Hours)')
    ax[2].set_xlabel('Time (UTC)')
    ax[2].set_ylabel('Wind Speed (m/s)')
    ax[2].grid(True)

    plt.tight_layout()
    return fig

# Streamlit app
def main():
    st.set_page_config(layout="centered")
    st.title("🌤️ Weather App 🌧️")
    
    # Use the provided API key
    api_key = "351f709097836804b66e2804cd6353cd"
    city = st.text_input("Enter city name")

    if st.button("Get Weather"):
        if not city:
            st.error("Please enter a city name")
        else:
            weather_data = get_weather(city, api_key)
            if weather_data.get("cod") != 200:
                st.error(weather_data.get("message"))
            else:
                st.success(f"Weather in {city}:")

                # Display weather icon
                icon_code = weather_data['weather'][0]['icon']
                weather_icon = get_weather_icon(icon_code)
                st.image(weather_icon)

                # Display weather information with emojis
                st.write(f"**🌡️ Temperature:** {weather_data['main']['temp']} °C")
                st.write(f"**☁️ Weather:** {weather_data['weather'][0]['description'].capitalize()}")
                st.write(f"**💧 Humidity:** {weather_data['main']['humidity']}%")
                st.write(f"**🌬️ Wind Speed:** {weather_data['wind']['speed']} m/s")
                st.write(f"**🌀 Air Pressure:** {weather_data['main']['pressure']} hPa")

                # Get historical weather data and plot graphs
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']
                historical_data = get_historical_weather(lat, lon, api_key)
                fig = plot_historical_data(historical_data, city)
                st.pyplot(fig)

if __name__ == "__main__":
    main()
