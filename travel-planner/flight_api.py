import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file (to store API keys securely)
load_dotenv()

# API key and endpoint URL
FLIGHT_API_KEY = os.getenv('FLIGHT_API_KEY')
FLIGHT_API_URL = f"https://api.flightapi.io/roundtrip/{FLIGHT_API_KEY}"

def get_flight_details(arrival_airport_code):
    # Set default values for departure airport and other parameters
    departure_airport_code = "MSP"
    departure_date = "2024-11-01"
    return_date = "2024-11-07"
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

# Function to extract and print the flight prices
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

# Example usage
if __name__ == "__main__":
    arrival_airport_code = input("Enter your destination airport code (e.g., LAX): ")
    
    # Fetch flight details with default values and the provided destination
    flight_data = get_flight_details(arrival_airport_code)
    
    # If data is fetched successfully, extract and display the unique prices
    if flight_data:
        get_unique_flight_prices(flight_data)
    else:
        print("No flight data available.")
