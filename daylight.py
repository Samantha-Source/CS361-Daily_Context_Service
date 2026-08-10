# Name: Craig Harker, Kelli Muldoon, & Samantha Brown
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Daylight source module. 
# Calls the sunrise-sunset.org API to get today's sunrisesunset for a given latitude and longitude.
# Works out wheter it is currently daytime there.

# Code Citation
# Adapted from: Sunrise-Sunset.org API Documentation
# Source URL: https://sunrise-sunset.org/api

"""
Daylight source. Owner: Samantha Brown
 
Calls an external sunrise/sunset API (sunrise-sunset.org) and
returns today's daylight window for a coordinate pair.
"""
 
from datetime import datetime, timezone

import requests

DAYLIGHT_URL = "https://api.sunrise-sunset.org/json"
DAYLIGHT_TIMEOUT_SECONDS = 5


def get_daylight(lat, lon):
    """
    Args:
        lat, lon: floats.
 
    Returns:
        dict, e.g.:
            {
                "sunrise": "2026-08-09T06:12:00Z", 
                "sunset": "2026-08-09T20:41:00Z",
                "is_daytime": True,
            }
        sunrise/sunset are today's times in UTC ISO 8601 with a "Z" suffix,
        is_daytime: wheter the current moment falls between sunrise and sunset
 
    Raises:
        Exception: on any failure (network error, bad response, timeout).
            Do not catch it here -- app.py's fetch_source() catches it
            and turns it into a per-source error so the rest of the
            /context response can still succeed.
    """

    response = requests.get(
        DAYLIGHT_URL,
        params={
            "lat": lat,
            "lng": lon,
            "formatted": 0,     # ISO 8601 timestamps instead of "7:12:00 AM"
        },
        timeout=DAYLIGHT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "OK":
        raise RuntimeError(f"sunrise-sunset.org returned status: {data.get('status')}")

    results = data["results"]
    sunrise_raw = results["sunrise"]
    sunset_raw = results["sunset"]

    # sunrise-sunset.org always returns UTC when formatted=0, so +00:00 can be normalized to "Z"
    sunrise_dt = datetime.fromisoformat(sunrise_raw)
    sunset_dt = datetime.fromisoformat(sunset_raw)
    now = datetime.now(timezone.utc)

    return {
        "sunrise": sunrise_raw.replace("+00:00", "Z"),
        "sunset": sunset_raw.replace("+00:00", "Z"),
        "is_daytime": sunrise_dt <= now <= sunset_dt,
    }