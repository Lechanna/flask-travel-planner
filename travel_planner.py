import requests
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys and base URLs
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
geo_base_url = "http://api.openweathermap.org/geo/1.0/direct"

# Use RESTAURANT_API_KEY for both restaurants and geocoding
RESTAURANT_API_KEY = os.getenv('RESTAURANT_API_KEY')
ATTRACTION_API_KEY = os.getenv('ATTRACTION_API_KEY')
ATTRACTION_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
RESTAURANT_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
GEOCODING_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

def get_weather(city, country):
    geo_params = {
        'q': f"{city},{country}",
        'appid': WEATHER_API_KEY,
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
            'appid': WEATHER_API_KEY,
            'units': 'imperial'
        }
        weather_url = f"{WEATHER_API_URL}?{urllib.parse.urlencode(weather_params)}"
    
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

def get_local_attractions(location, radius=1000, type='tourist_attraction'):
    params = {
        'location': location,
        'radius': radius,
        'type': type,
        'key': ATTRACTION_API_KEY  # Using the same key for geocoding and attractions
    }
    response = requests.get(ATTRACTION_API_URL, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        attractions = [(place['name'], place.get('rating', 'No rating')) for place in results]
        return attractions
    else:
        return []

def get_restaurant_recommendations(location, radius=1500, type='restaurant'):
    params = {
        'location': location,
        'radius': radius,
        'type': type,
        'key': RESTAURANT_API_KEY
    }
    response = requests.get(RESTAURANT_API_URL, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        restaurants = [(place['name'], place.get('rating', 'No rating')) for place in results]
        return restaurants
    else:
        return []

def main():
    city = input("Enter a City: ")
    country = input("Enter the country or state of the city: ")

    # Get weather information
    get_weather(city, country)

    # Geocode the location for attractions and restaurants
    user_location_name = f"{city},{country}"
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={user_location_name}&key={ATTRACTION_API_KEY}"
    geocode_response = requests.get(geocode_url)
    
    if geocode_response.status_code == 200:
        geocode_results = geocode_response.json().get('results', [])
        if geocode_results:
            location = geocode_results[0]['geometry']['location']
            user_location = f"{location['lat']},{location['lng']}"
        else:
            print("Location not found.")
            print(f"Geocode API response: {geocode_response.json()}")
            return
    else:
        print(f"Geocode API response: {geocode_response.json()}")
        print("Error in geocoding the location.")
        return

    # Get local attractions and restaurant recommendations
    attractions = get_local_attractions(user_location)
    attractions.sort(key=lambda x: float(x[1]) if x[1] != 'No rating' else 0, reverse=True)
    print("\nLocal Attractions:")
    for name, rating in attractions:
        print(f"{name} - Rating: {rating}")

    restaurants = get_restaurant_recommendations(user_location)
    restaurants.sort(key=lambda x: float(x[1]) if x[1] != 'No rating' else 0, reverse=True)
    print("\nRestaurant Recommendations:")
    for name, rating in restaurants:
        print(f"{name} - Rating: {rating}")

if __name__ == "__main__":
    main()

