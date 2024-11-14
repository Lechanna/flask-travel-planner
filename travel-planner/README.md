# Travel Itinerary Planner

This project is a comprehensive travel itinerary planner that integrates multiple APIs to provide the following:

- Weather Information (via OpenWeather API)
- Restaurant Recommendations (via Restaurant API)
- Attraction Suggestions (via Attractions API)
- Flight Information (via Flight API)
  
The script allows users to input a destination city and country, after which it retrieves weather, restaurants, attractions, and flight details based on that input. All API keys are securely managed through environment variables.

----------------------------------------------------------------------------------------
**Features:**

Weather API: Get current weather data for the destination.

Restaurant API: Receive restaurant recommendations in the destination city.

Attractions API: Fetch recommended tourist attractions in the area.

Flight API: Get flight prices from a default departure location to the destination.

---------------------------------------------------------------------------
**Requirements**
Python 3.x
requests library
API keys for each service (stored in an .env file)


------------------------------------------------------------------------
**Installation**
1. Clone the repository:

    git clone https://github.com/cardellak5813/travel-planner

    cd your-repo-name



2. Create a virtual environment (optional but recommended):

      python -m venv env
   
      source env/bin/activate  # For Windows: env\Scripts\activate


  
3. Install dependencies:

      pip install -r requirements.txt
   

4. Set up the environment variables by creating a .env file (see Environment Variables).

---------------------------------------------------------------------------------------------
**Usage**

1. Run the script:

      python travel_planner.py


2. Input the required details:

- City and country
- Flight details (departure, arrival airport codes, number of passengers, etc.)

  
3. Receive travel recommendations:

      The script will fetch and display the weather forecast, restaurant and attraction suggestions, and flight prices.

-----------------------------------------------------------------------------------------
**Environment Variables**
The project uses environment variables to securely store API keys. You'll need to create a .env file in the project root directory with the following content:

    FLIGHT_API_KEY=your_flight_api_key
    RESTAURANT_API_KEY=your_restaurant_api_key
    WEATHER_API_KEY=your_weather_api_key
    ATTRACTIONS_API_KEY=your_attractions_api_key
  
  Replace your_x_api_key with the actual API keys.

  -------------------------------------------------------------------------------------------------

**Flight API Example**

The flight API fetches flight data using default parameters (e.g., departure from MSP, economy class) for a round-trip to the destination. The script uses the following default values:

Departure Airport: MSP (Minneapolis, MN)

Arrival Airport: User-provided

Dates: Default dates of 11/1/24 - 11/7/24


**Example output:**

Enter your destination airport code (e.g., LAX): SFO

Top 5 Flight Prices:
1. $350.00
2. $400.50
3. $420.75
4. $450.00
5. $470.25
