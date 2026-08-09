# Name: Craig Harker, Kelli Muldoon, & Samantha Brown
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Weather source module. Calls an external weather API and
#   returns current conditions for a coordinate pair.
 
"""
Weather source. Owner: fill in your name here.
 
Calls an external weather API (e.g. OpenWeatherMap, National Weather
Service) and returns current conditions for a coordinate pair.
"""
 
 
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
    raise NotImplementedError("weather fetch not yet implemented")