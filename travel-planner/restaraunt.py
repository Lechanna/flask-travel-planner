import requests
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys and Base URLs
RESTAURANT_API_KEY = os.getenv('RESTAURANT_API_KEY')
RESTAURANT_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

# Function to get restaurant recommendations based on location
def get_restaurant_recommendations(location, radius=1500, type='restaurant'):
    params = {
        'location': location,
        'radius': radius,
        'type': type,
        'key': RESTAURANT_API_KEY
    }
    
    # Make the API request to Google Places API
    response = requests.get(RESTAURANT_API_URL, params=params)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        restaurants = [(place['name'], place.get('rating', 'No rating')) for place in results]
        return restaurants
    else:
        return []

# Function to recommend restaurants based on city and country
def recommend_restaurants(city, country):
    # Geocoding the location name to get latitude and longitude
    user_location_name = f"{city},{country}"
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(user_location_name)}&key={RESTAURANT_API_KEY}"
    geocode_response = requests.get(geocode_url)
    
    if geocode_response.status_code == 200:
        geocode_results = geocode_response.json().get('results', [])
        if geocode_results:
            # Extracting latitude and longitude
            location = geocode_results[0]['geometry']['location']
            user_location = f"{location['lat']},{location['lng']}"
            
            # Fetching restaurant recommendations based on geocoded location
            restaurants = get_restaurant_recommendations(user_location)
            
            # Sorting restaurants by rating (if available)
            restaurants.sort(key=lambda x: float(x[1]) if x[1] != 'No rating' else 0, reverse=True)
            
            print(f"Restaurant recommendations in {user_location_name}:")
            if restaurants:
                for name, rating in restaurants:
                    print(f"{name} - Rating: {rating}")
            else:
                print("No restaurants found.")
        else:
            print("Location not found.")
    else:
        print("Error in geocoding the location.")


