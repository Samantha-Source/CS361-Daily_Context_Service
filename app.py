# Name: Craig Harker, Kelli Muldoon, & Samantha Brown
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Main Flask app for the Daily Context microservice. Defines
#   the /health and /context endpoints, resolves the requested location,
#   fetches weather/air quality/daylight concurrently, and merges the
#   results into a single response with partial-failure support.
 
"""
Daily Context Service
Merges weather, air quality, and daylight data for a given location.
 
Endpoints:
    GET /health   - service liveness check
    GET /context  - merged weather/air-quality/daylight snapshot
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
 
from dotenv import load_dotenv
from flask import Flask, jsonify, request
 
from location import resolve_location, LocationError
import weather
import air_quality
import daylight
 
load_dotenv()
 
app = Flask(__name__)

# Let browser-based main programs call this service
@app.after_request
def allow_main_program(response):
    configured = os.eniron.get(
        "MAIN_PROGRAM_ORIGINS",
        os.environ.get(
            "MAIN_PROGRAM_ORIGIN",
            "http://localhost:5173, http://127.0.0.1:5173",
        ),
    )
    allowed = {
        value.strip().rstrip("/") for value in configured.split(",") if value.strip()
    }
    origin = (request.headers.get("Origin") or "").rstrip("/")
    if origin in allowed:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,OPTIONS"
    return response
 
# Maps a name in the merged response to the function that produces it.
# Each function must accept (lat, lon) and return a dict, or raise an
# exception on failure -- fetch_source() below catches it and turns it
# into a per-source error instead of failing the whole request.
SOURCES = {
    "weather": weather.get_weather,
    "air_quality": air_quality.get_air_quality,
    "daylight": daylight.get_daylight,
}
 
 
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200
 
 
def fetch_source(name, fn, lat, lon):
    """Run one source fetch and normalize failures into an error dict
    instead of letting an exception take down the whole request."""
    try:
        return name, fn(lat, lon), None
    except Exception as exc:  # noqa: BLE001 - intentionally broad, see docstring
        return name, None, str(exc)
 
 
@app.route("/context", methods=["GET"])
def context():
    location_input = request.args.get("location", "")
 
    try:
        lat, lon = resolve_location(location_input)
    except LocationError as exc:
        return jsonify({"error": str(exc)}), 400
 
    results = {}
    had_failure = False
 
    # Fetch all three sources concurrently to stay near the ~1s target.
    with ThreadPoolExecutor(max_workers=len(SOURCES)) as executor:
        futures = [
            executor.submit(fetch_source, name, fn, lat, lon)
            for name, fn in SOURCES.items()
        ]
        for future in as_completed(futures):
            name, data, error = future.result()
            if error:
                had_failure = True
                results[name] = {"error": error}
            else:
                results[name] = data
 
    response = {
        "location": {"input": location_input, "lat": lat, "lon": lon},
        **results,
        "partial": had_failure,
    }
    return jsonify(response), 200
 
 
if __name__ == "__main__":
    app.run(port=5106, debug=True)