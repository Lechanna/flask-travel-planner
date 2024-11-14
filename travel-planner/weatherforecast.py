import requests
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

# API keys and base URLs
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Get user input
city = input("Enter a City: ")
country = input("Enter the country or state of the city: ")

# API key and base URL
WEATHER_API_KEY = "e370c1f80781f24e8110649eba4b6329"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Construct the full API URL
params = {
    'q': f"{city},{country}",
    'appid': WEATHER_API_KEY,
    'units': 'imperial'
}
url = f"{WEATHER_API_URL}?{urllib.parse.urlencode(params)}"

# Make the API call
response = requests.get(url)
data = response.json()

# Check if the response contains 'weather' data
if response.status_code == 200 and 'weather' in data:
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    print(f"The weather in {city}, {country} is {weather_description} with a temperature of {temperature}°F.")
else:
    print("Error fetching weather data. Please check the city and country/state names.")
