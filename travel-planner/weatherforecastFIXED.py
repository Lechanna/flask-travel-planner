import requests
import urllib.parse

# Get user input
city = input("Enter a City: ")
country = input("Enter the country or state of the city: ")

# API key and base URL
weatherKey = "e370c1f80781f24e8110649eba4b6329"
geo_base_url = "http://api.openweathermap.org/geo/1.0/direct"
weather_base_url = "http://api.openweathermap.org/data/2.5/weather"

# Construct the full API URL to get latitude and longitude
geo_params = {
    'q': f"{city},{country}",
    'appid': weatherKey,
    'limit': '1'
}
geo_url = f"{geo_base_url}?{urllib.parse.urlencode(geo_params)}"

# Make the API call to get latitude and longitude
geo_response = requests.get(geo_url)
geo_data = geo_response.json()

# Check if the response contains 'lat' and 'lon' data
if geo_response.status_code == 200 and len(geo_data) > 0:
    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']
    
    # Construct the full API URL to get current weather data
    weather_params = {
        'lat': lat,
        'lon': lon,
        'appid': weatherKey,
        'units': 'imperial'
    }
    weather_url = f"{weather_base_url}?{urllib.parse.urlencode(weather_params)}"
    
    # Make the API call to get current weather data
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    # Check if the response contains weather data
    if weather_response.status_code == 200:
        print(f"Current weather in {city}, {country}:")
        print(f"Temperature: {weather_data['main']['temp']}°F")
        print(f"Weather: {weather_data['weather'][0]['description']}")
    else:
        print("Error fetching weather data.")
else:
    print("Error fetching location data. Please check the city and country/state names.")