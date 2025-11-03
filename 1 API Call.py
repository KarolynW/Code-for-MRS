"""Simple weather API example for market researchers.

This script calls the public `open-meteo.com` weather API to fetch the
current weather for London.  The goal is to show what a basic API request
looks like and how to read the JSON response that comes back.

How to run in VS Code
---------------------
1. Open VS Code and choose **File > Open Folder...**, then select the
   `Code-for-MRS` folder that contains this file.
2. In the Explorer panel click `1 API Call.py` to open it.
3. Ensure you have the Python extension installed (VS Code may prompt you).
4. Click the green **Run Python File** button in the top-right of the editor
   window, or press ``Ctrl+F5`` (``Cmd+F5`` on macOS).
5. The output will appear in the **Python Terminal** pane at the bottom of VS
   Code.

No API keys or extra setup are required for this example.  The `requests`
library comes pre-installed with most Python distributions, but if you see an
error you can install it by running `pip install requests` in the terminal.
"""

from typing import Any, Dict

import requests

# -----------------------------
# 1. Define the API end point.
# -----------------------------
# This URL tells requests which server to talk to.
URL = "https://api.open-meteo.com/v1/forecast"

# --------------------------------------------------------------------
# 2. Build the query string (the information we send to the API).
# --------------------------------------------------------------------
# Each key/value pair becomes part of the web request so the service knows
# what data to return.  Here we ask for London's current weather.
PARAMS: Dict[str, Any] = {
    "latitude": 51.5072,     # North/South location (51.5° N)
    "longitude": -0.1276,    # East/West location (0.12° W)
    "current_weather": True  # Tell the API we want the "current_weather" block
}

try:
    # ------------------------------------------------------------------
    # 3. Send the GET request and raise an error if the server complains.
    # ------------------------------------------------------------------
    response = requests.get(URL, params=PARAMS, timeout=10)
    response.raise_for_status()

    # ---------------------------------------------------------------
    # 4. Convert the JSON text returned by the server into Python data.
    # ---------------------------------------------------------------
    data = response.json()

    print("✅ Successful API Call!\n")
    print("Raw JSON Response:")
    print(data)

    # ---------------------------------------------------------------
    # 5. Pull out a useful section from the JSON (`current_weather`).
    # ---------------------------------------------------------------
    current_weather = data["current_weather"]
    print("\nCurrent Weather in London:")
    print(f"Temperature: {current_weather['temperature']}°C")
    print(f"Windspeed: {current_weather['windspeed']} km/h")

except requests.exceptions.HTTPError as error:
    # Something about the request was incorrect (e.g., wrong URL).
    print(f"❌ HTTP error: {error}")
except requests.exceptions.RequestException as error:
    # Handles network problems such as no internet connection.
    print(f"❌ Network or API error: {error}")
