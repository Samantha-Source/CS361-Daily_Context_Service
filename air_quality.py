# Name: Craig Harker, Kelli Muldoon, & Samantha Brown
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Air quality source module. Calls an external air quality
#   API and returns current AQI for a coordinate pair.
 
"""
Air quality source. Owner: fill in your name here.
 
Calls an external air quality API (e.g. OpenWeatherMap Air Pollution,
AirNow, Open-Meteo) and returns current AQI for a coordinate pair.
"""
 
 
def get_air_quality(lat, lon):
    """
    Args:
        lat, lon: floats.
 
    Returns:
        dict, e.g.:
            {"aqi": 32, "category": "Good"}
 
    Raises:
        Exception: on any failure (network error, bad response, timeout).
            Do not catch it here -- app.py's fetch_source() catches it
            and turns it into a per-source error so the rest of the
            /context response can still succeed.
    """
    raise NotImplementedError("air quality fetch not yet implemented")
 