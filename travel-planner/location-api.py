import requests
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

# API keys and base URLs
ATTRACTION_API_KEY = os.getenv('ATTRACTION_API_KEY')
ATTRACTION_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

def get_local_attractions(location, radius=1000, type='tourist_attraction'):
    params = {
        'location': location,
        'radius': radius,
        'type': type,
        'key': ATTRACTION_API_KEY
    }
    
    response = requests.get(ATTRACTION_API_URL, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        attractions = [(place['name'], place.get('rating', 'No rating')) for place in results]
        return attractions
    else:
        return []

if __name__ == "__main__":
    user_location_name = input("Enter your location: ")
    params = {
        'rankby': 'prominence',
        'maxresults': 20
    }
    # Geocoding the location name to get latitude and longitude
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={user_location_name}&key={ATTRACTION_API_KEY}"
    geocode_response = requests.get(geocode_url)
    
    if geocode_response.status_code == 200:
        geocode_results = geocode_response.json().get('results', [])
        if geocode_results:
            location = geocode_results[0]['geometry']['location']
            user_location = f"{location['lat']},{location['lng']}"
        else:
            print("Location not found.")
            exit(1)
    else:
        print("Error in geocoding the location.")
        exit(1)
    attractions = get_local_attractions(user_location)
    attractions.sort(key=lambda x: float(x[1]) if x[1] != 'No rating' else 0, reverse=True)
    print("Local Attractions:")
    for name, rating in attractions:
        print(f"{name} - Rating: {rating}")
