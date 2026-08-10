# Name: Kelli Muldoon
# Course: CS361 - Software Engineering 1
# File: air_quality.py
# Due Date: 8/10/26
# Description: Air quality source module. Calls Open-Meteo to get air quality
# for a given latitude and longitude.

# Code Citation
# Adapted from: Open-Meteo Air Quality API Documentation
# Source URL: https://open-meteo.com/en/docs/air-quality-api

# Code Citation
# Adapted from: AirNow - AQI Basics, U.S. Environmental Protection Agency
# Source URL: https://www.airnow.gov/aqi/aqi-basics/

import requests


AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
AIR_QUALITY_TIMEOUT_SECONDS = 5


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

    response = requests.get(
        AIR_QUALITY_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "us_aqi"
        },
        timeout=AIR_QUALITY_TIMEOUT_SECONDS
    )

    response.raise_for_status()
    data = response.json()
    aqi = data["current"]["us_aqi"]
    if aqi <= 50:
        category = "Good"
    elif aqi <= 100:
        category = "Moderate"
    elif aqi <= 150:
        category = "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        category = "Unhealthy"
    elif aqi <= 300:
        category = "Very Unhealthy"
    else:
        category = "Hazardous"

    return {"aqi": aqi, "category": category}
