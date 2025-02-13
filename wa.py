import streamlit as st
import requests

# Function to get weather data
def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

# Streamlit app
def main():
    st.title("Weather App")
    
    # Use the provided API key
    api_key = "351f709097836804b66e2804cd6353cd"  # Ensure this is the correct API key
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
                st.write(f"Temperature: {weather_data['main']['temp']} °C")
                st.write(f"Weather: {weather_data['weather'][0]['description'].capitalize()}")
                st.write(f"Humidity: {weather_data['main']['humidity']}%")
                st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")

if __name__ == "__main__":
    main()
