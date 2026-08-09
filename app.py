# Name: Craig Harker, Kelli Muldoon, & Samantha Brown
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Resolves a user-supplied location string (city name, zip
#   code, or "lat,long") into coordinates via direct parsing or a
#   geocoding provider, for use by the /context endpoint.
 
"""
Resolves a user-supplied location string (city name, zip code, or
"lat,long") into coordinates the source modules can use.
"""
 
 
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
    Resolve a city name or zip code to coordinates via a geocoding API
    (OpenWeatherMap Geocoding, Nominatim).
 
    TODO: call the chosen geocoding provider here. Raise LocationError
    with a clear message if the provider returns no results.
    """
    raise NotImplementedError("geocoding not yet implemented")