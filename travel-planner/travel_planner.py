import requests
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys and base URLs
FLIGHT_API_KEY = os.getenv('FLIGHT_API_KEY')
FLIGHT_API_URL = f"https://api.flightapi.io/roundtrip/{FLIGHT_API_KEY}"

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

# Use RESTAURANT_API_KEY for both restaurants and geocoding
RESTAURANT_API_KEY = os.getenv('RESTAURANT_API_KEY')
ATTRACTION_API_KEY = os.getenv('ATTRACTION_API_KEY')
ATTRACTION_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
RESTAURANT_API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
GEOCODING_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

# Flight API function
def get_flight_details(arrival_airport_code):
    # Set default values for departure airport and other parameters
    departure_airport_code = "MSN"  # Default departure airport (Madison, WI)
    departure_date = "2024-12-23"
    return_date = "2024-12-30"
    adults = 1
    children = 0
    infants = 0
    cabin_class = "Economy"
    currency = "USD"

    # Construct the full API URL with parameters
    url = f"{FLIGHT_API_URL}/{departure_airport_code}/{arrival_airport_code}/{departure_date}/{return_date}/{adults}/{children}/{infants}/{cabin_class}/{currency}"

    # Make the API request
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for any bad status codes (4xx, 5xx)
        flight_data = response.json()

        # Return the full response data for further use
        return flight_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching flight data: {e}")
        return None


# Function to extract and print flight prices
def get_unique_flight_prices(data):
    if "itineraries" in data:
        prices = set()  # Use a set to avoid duplicate prices
        for itinerary in data["itineraries"]:
            for option in itinerary["pricing_options"]:
                price = option["price"]["amount"]
                prices.add(price)

        # Convert the set to a sorted list and limit the output to 5 prices
        sorted_prices = sorted(prices)[:5]
        print("Top 5 Flight Prices:")
        for idx, price in enumerate(sorted_prices, 1):
            print(f"{idx}. ${price:.2f}")
    else:
        print("No pricing options available.")

def get_weather(city, country):
    params = {
        'q': f"{city},{country}",
        'appid': WEATHER_API_KEY,
        'units': 'imperial'
    }
    url = f"{WEATHER_API_URL}?{urllib.parse.urlencode(params)}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and 'weather' in data:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        print(f"The weather in {city}, {country} is {weather_description} with a temperature of {temperature}°F.")
    else:
        print("Error fetching weather data. Please check the city and country names.")

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

    # Get flight details
    arrival_airport_code = input("\nEnter your destination airport code: ")
    flight_data = get_flight_details(arrival_airport_code)
    if flight_data:
        get_unique_flight_prices(flight_data)
    else:
        print("No flight data available.")


if __name__ == "__main__":
    main()

