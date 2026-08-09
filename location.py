# Name: Craig Harker, Kelli Muldoon, & Samantha Brown
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Resolves a user-supplied location string (city name, zip
#   code, or "lat,long") into coordinates via direct parsing or a
#   geocoding provider, for use by the /context endpoint.

 
import os
import requests

GEOCODING_BASE_URL = "http://api.openweathermap.org/geo/1.0"
GEOCODING_TIMEOUT_SECONDS = 5


class LocationError(Exception):
    """Raised when a location string can't be resolved to coordinates."""
 
 
def resolve_location(location_input):
    """
    Args:
        location_input: raw string from the ?location= query param.
            Examples: "Corvallis,OR", "97330", "44.5646,-123.2620"
 
    Returns:
        (lat, lon) tuple of floats.
 
    Raises:
        LocationError: if location_input is empty, malformed, or can't
            be resolved by the geocoding provider.
    """
    if not location_input:
        raise LocationError("location parameter is required")
 
    coords = _try_parse_lat_long(location_input)
    if coords:
        return coords
 
    return _geocode(location_input)
 
 
def _try_parse_lat_long(location_input):
    """Return (lat, lon) if location_input is already a 'lat,long' pair,
    otherwise return None so the caller falls through to geocoding."""
    parts = location_input.split(",")
    if len(parts) != 2:
        return None
    try:
        lat, lon = float(parts[0].strip()), float(parts[1].strip())
    except ValueError:
        return None
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise LocationError(f"lat/long out of range: {location_input}")
    return lat, lon
 
 
def _geocode(location_input):
    """
    Resolve a city name or zip code to coordinates using OpenWeatherMap's
    Geocoding API. Auto-detects which endpoint to use: input that is all
    digits (optionally with a country code, e.g. "97330,US") is treated
    as a zip/postal code; anything else is treated as a city name.
 
    Raises:
        LocationError: if the API key is missing, the request fails, or
            the provider returns no results for this input.
    """
    api_key = os.environ.get("GEOCODING_API_KEY")
    if not api_key:
        raise LocationError("geocoding is not configured (missing API key)")
 
    zip_part = location_input.split(",")[0].strip()
    if zip_part.isdigit():
        return _geocode_zip(location_input, api_key)
    return _geocode_city(location_input, api_key)
 
 
def _geocode_zip(location_input, api_key):
    """Resolve a zip/postal code (e.g. "97330" or "97330,US") via the
    OpenWeatherMap zip endpoint. Defaults to country code US if none is
    given, since that's the common case for this project."""
    zip_query = location_input if "," in location_input else f"{location_input},US"
    try:
        resp = requests.get(
            f"{GEOCODING_BASE_URL}/zip",
            params={"zip": zip_query, "appid": api_key},
            timeout=GEOCODING_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise LocationError(f"geocoding request failed: {exc}") from exc
 
    if resp.status_code == 404:
        raise LocationError(f"unrecognized zip code: {location_input}")
    if not resp.ok:
        raise LocationError(f"geocoding provider error: {resp.status_code}")
 
    data = resp.json()
    if "lat" not in data or "lon" not in data:
        raise LocationError(f"unrecognized zip code: {location_input}")
    return data["lat"], data["lon"]
 
 
def _geocode_city(location_input, api_key):
    """Resolve a city name (e.g. "Corvallis,OR" or "Corvallis,OR,US")
    via the OpenWeatherMap direct geocoding endpoint."""
    try:
        resp = requests.get(
            f"{GEOCODING_BASE_URL}/direct",
            params={"q": location_input, "limit": 1, "appid": api_key},
            timeout=GEOCODING_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise LocationError(f"geocoding request failed: {exc}") from exc
 
    if not resp.ok:
        raise LocationError(f"geocoding provider error: {resp.status_code}")
 
    results = resp.json()
    if not results:
        raise LocationError(f"unrecognized location: {location_input}")
    return results[0]["lat"], results[0]["lon"]