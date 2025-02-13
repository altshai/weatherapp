import streamlit as st
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO

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

# Function to get weather icon
def get_weather_icon(icon_code):
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
    response = requests.get(icon_url)
    return Image.open(BytesIO(response.content))

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
                
                # Background image based on weather
                weather_main = weather_data['weather'][0]['main'].lower()
                if weather_main in ["clear", "clouds"]:
                    bg_image_url = "https://example.com/clear_clouds.jpg"
                elif weather_main in ["rain", "drizzle"]:
                    bg_image_url = "https://example.com/rain_drizzle.jpg"
                elif weather_main in ["snow"]:
                    bg_image_url = "https://example.com/snow.jpg"
                else:
                    bg_image_url = "https://example.com/default.jpg"
                
                st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background-image: url({data:image/jpeg;base64,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});
                        background-size: cover;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()
