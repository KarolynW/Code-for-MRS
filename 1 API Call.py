import requests

# Example: Open-Meteo API (no API key required)
url = "https://api.open-meteo.com/v1/forecast"

# Parameters (what we’re sending)
params = {
    "latitude": 51.5072,     # London
    "longitude": -0.1276,
    "current_weather": True  # ask for current weather data
}

try:
    # Send GET request to the API
    response = requests.get(url, params=params)
    response.raise_for_status()  # raise an error for bad responses

    # Parse the JSON reply
    data = response.json()

    print("✅ Successful API Call!\n")
    print("Raw JSON Response:")
    print(data)

    # Extract a useful bit of data
    current_weather = data["current_weather"]
    print("\nCurrent Weather in London:")
    print(f"Temperature: {current_weather['temperature']}°C")
    print(f"Windspeed: {current_weather['windspeed']} km/h")

except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"❌ Network or API error: {e}")