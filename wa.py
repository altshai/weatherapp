import streamlit as st
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO
from streamlit_lottie import st_lottie

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

# Function to load Lottie animations
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

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

                # Display weather information with icons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st_lottie(load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_kq5rGs.json"), height=100, key="temperature")
                    st.metric(label="Temperature", value=f"{weather_data['main']['temp']} °C")
                
                with col2:
                    st_lottie(load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_J5Gh0V.json"), height=100, key="humidity")
                    st.metric(label="Humidity", value=f"{weather_data['main']['humidity']}%")
                
                with col3:
                    st_lottie(load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_6unl4hkp.json"), height=100, key="wind")
                    st.metric(label="Wind Speed", value=f"{weather_data['wind']['speed']} m/s")

                st_lottie(load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_y1ymv1n4.json"), height=100, key="pressure")
                st.metric(label="Air Pressure", value=f"{weather_data['main']['pressure']} hPa")

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
                        background-image: url({bg_image_url});
                        background-size: cover;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()
