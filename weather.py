# Name: Craig Harker, Kelli Muldoon, & Samantha Brown
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Weather source module. Calls an external weather API and
#   returns current conditions for a coordinate pair.

# Code Citation
# Adapted from : OpenWeatherMap Current Weater Data API Documentation
# Source URL: https://openweathermap.org/current
 
"""
Weather source. Owner: Samantha Brown
 
Calls an external weather API (OpenWeatherMap) and returns current conditions for a coordinate pair.
"""

import os
import requests

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
WEATHER_TIMEOUT_SECONDS = 5
 
 
def get_weather(lat, lon):
    """
    Args:
        lat, lon: floats.
 
    Returns:
        dict, e.g.:
            {"temp_f": 72, "condition": "Partly cloudy"}
 
    Raises:
        Exception: on any failure (network error, bad response, timeout).
            Do not catch it here -- app.py's fetch_source() catches it
            and turns it into a per-source error so the rest of the
            /context response can still succeed.
    """

    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("weather is not configured (missing WEATHER_API_KEY)")

    response = requests.get(
        WEATHER_URL,
        params={
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "imperial",    #temp_f in the response contract, so ask for Fahrenheit directly
        },
        timeout=WEATHER_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data = response.json()

    temp_f = data["main"]["temp"]
    condition = data["weather"][0]["description"].capitalize()

    return {"temp_f": round(temp_f), "condition": condition}
