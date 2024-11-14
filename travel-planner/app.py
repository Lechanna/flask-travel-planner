from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# API keys and base URLs
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"
ATTRACTION_API_KEY = os.getenv('ATTRACTION_API_KEY')
ATTRACTION_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
RESTAURANT_API_KEY = os.getenv('RESTAURANT_API_KEY')
RESTAURANT_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def get_results():
    city = request.form['city']
    state = request.form['state']
    print(f"Received city: {city}, state: {state}")  # Debugging line to check form values
    location = f"{city},{state}"
    weather_info = get_weather(location)
    attractions = get_attractions(location)
    restaurants = get_restaurants(location)
    
    return render_template('itinerary.html', weather_info=weather_info, attractions=attractions, restaurants=restaurants)

def get_weather(location):
    geo_params = {
        'q': location,
        'appid': WEATHER_API_KEY,
        'limit': '1'
    }
    geo_url = f"{GEOCODING_API_URL}?{urllib.parse.urlencode(geo_params)}"

    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if geo_response.status_code == 200 and len(geo_data) > 0:
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
    
        weather_params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'imperial'
        }
        weather_url = f"{WEATHER_API_URL}?{urllib.parse.urlencode(weather_params)}"
    
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
    
        if weather_response.status_code == 200:
            return f"Current weather in {location} is {weather_data['main']['temp']}°F with {weather_data['weather'][0]['description']}"
        else:
            return "Error fetching weather data."
    else:
        return "Error fetching location data. Please check the city and country/state names."

def get_attractions(location):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={ATTRACTION_API_KEY}"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()
    
    if geocode_response.status_code == 200 and geocode_data['results']:
        location_coords = geocode_data['results'][0]['geometry']['location']
        user_location = f"{location_coords['lat']},{location_coords['lng']}"
        params = {
            'location': user_location,
            'radius': 5000,
            'type': 'tourist_attraction',
            'key': ATTRACTION_API_KEY
        }
        url = f"{ATTRACTION_API_URL}?{urllib.parse.urlencode(params)}"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and 'results' in data:
            attractions = [(place['name'], place.get('rating', 'No rating')) for place in data['results']]
            attractions.sort(key=lambda x: float(x[1]) if x[1] != 'No rating' else 0, reverse=True)
            return attractions
        else:
            return []
    else:
        return []

def get_restaurants(location):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={RESTAURANT_API_KEY}"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()
    
    if geocode_response.status_code == 200 and geocode_data['results']:
        location_coords = geocode_data['results'][0]['geometry']['location']
        user_location = f"{location_coords['lat']},{location_coords['lng']}"
        params = {
            'location': user_location,
            'radius': 5000,
            'type': 'restaurant',
            'key': RESTAURANT_API_KEY
        }
        url = f"{RESTAURANT_API_URL}?{urllib.parse.urlencode(params)}"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and 'results' in data:
            restaurants = [(place['name'], place.get('rating', 'No rating')) for place in data['results']]
            restaurants.sort(key=lambda x: float(x[1]) if x[1] != 'No rating' else 0, reverse=True)
            return restaurants
        else:
            return []
    else:
        return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
