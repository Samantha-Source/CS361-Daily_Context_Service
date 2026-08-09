# Name: Craig Harker, Kelli Muldoon, & Samantha Brown
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Daylight source module. Calls an external sunrise/sunset
#   API and returns today's daylight window for a coordinate pair.
 
"""
Daylight source. Owner: fill in your name here.
 
Calls an external sunrise/sunset API (e.g. sunrise-sunset.org) and
returns today's daylight window for a coordinate pair.
"""
 
 
def get_daylight(lat, lon):
    """
    Args:
        lat, lon: floats.
 
    Returns:
        dict, e.g.:
            {"sunrise": "2026-08-09T06:12:00Z", "sunset": "2026-08-09T20:41:00Z"}
 
    Raises:
        Exception: on any failure (network error, bad response, timeout).
            Do not catch it here -- app.py's fetch_source() catches it
            and turns it into a per-source error so the rest of the
            /context response can still succeed.
    """
    raise NotImplementedError("daylight fetch not yet implemented")