# Name: Craig Harker, Kelli Muldoon, & Samantha Brown
# Course: CS361 - Software Engineering 1
# Assignment: Assignment 9
# Due Date: 8/10/26
# Description: Tests for the Daily Context microservice -- core /context
#   endpoint (location parsing, concurrent fetch, partial-result
#   behavior) plus the weather, air quality, and daylight source
#   modules. Each source's tests mock its external API call.
 
import pytest
 
from app import app
from location import resolve_location, LocationError
import weather
import air_quality
import daylight
 
 
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
 
 
# ---------------------------------------------------------------------
# Core /context endpoint and location parsing
# Owner: Craig
# ---------------------------------------------------------------------
 
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}
 
 
def test_context_missing_location(client):
    resp = client.get("/context")
    assert resp.status_code == 400
    assert "error" in resp.get_json()
 
 
def test_context_lat_long_passthrough(client, monkeypatch):
    """A 'lat,long' location should skip geocoding entirely."""
    monkeypatch.setattr(
        "app.SOURCES",
        {
            "weather": lambda lat, lon: {"temp_f": 70},
            "air_quality": lambda lat, lon: {"aqi": 10},
            "daylight": lambda lat, lon: {"sunrise": "x", "sunset": "y"},
        },
    )
    resp = client.get("/context?location=44.56,-123.26")
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["partial"] is False
    assert body["weather"] == {"temp_f": 70}
 
 
def test_context_partial_on_source_failure(client, monkeypatch):
    """If one source raises, the response should still include the
    other two and set partial=True."""
 
    def failing_source(lat, lon):
        raise RuntimeError("simulated failure")
 
    monkeypatch.setattr(
        "app.SOURCES",
        {
            "weather": lambda lat, lon: {"temp_f": 70},
            "air_quality": failing_source,
            "daylight": lambda lat, lon: {"sunrise": "x", "sunset": "y"},
        },
    )
    resp = client.get("/context?location=44.56,-123.26")
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["partial"] is True
    assert "error" in body["air_quality"]
    assert body["weather"] == {"temp_f": 70}
 
 
# ---------------------------------------------------------------------
# Geocoding (location.py's _geocode, _geocode_zip, _geocode_city)
# Owner: Craig
# ---------------------------------------------------------------------
 
from location import _geocode_zip, _geocode_city
 
 
def test_geocode_missing_api_key(monkeypatch):
    monkeypatch.delenv("GEOCODING_API_KEY", raising=False)
    with pytest.raises(LocationError):
        resolve_location("Corvallis,OR")
 
 
def test_geocode_city_no_results(monkeypatch):
    """Provider returning an empty list should raise LocationError."""
 
    class FakeResponse:
        ok = True
        status_code = 200
 
        def json(self):
            return []
 
    monkeypatch.setattr("requests.get", lambda *a, **k: FakeResponse())
    with pytest.raises(LocationError):
        _geocode_city("Nowhereville", "test-key")
 
 
def test_geocode_zip_not_found(monkeypatch):
    """A 404 from the zip endpoint should raise LocationError."""
 
    class FakeResponse:
        ok = False
        status_code = 404
 
        def json(self):
            return {}
 
    monkeypatch.setattr("requests.get", lambda *a, **k: FakeResponse())
    with pytest.raises(LocationError):
        _geocode_zip("00000", "test-key")
 
 
def test_geocode_routes_zip_vs_city(monkeypatch):
    """Digit input should hit the zip endpoint; text input should hit
    the city (direct) endpoint."""
    monkeypatch.setenv("GEOCODING_API_KEY", "test-key")
 
    calls = []
    monkeypatch.setattr(
        "location._geocode_zip",
        lambda loc, key: calls.append(("zip", loc)) or (44.5, -123.2),
    )
    monkeypatch.setattr(
        "location._geocode_city",
        lambda loc, key: calls.append(("city", loc)) or (44.5, -123.2),
    )
 
    resolve_location("97330")
    resolve_location("Corvallis,OR")
 
    assert calls == [("zip", "97330"), ("city", "Corvallis,OR")]
 
 
# ---------------------------------------------------------------------
# Weather source (sources/weather.py)
# Owner: Samantha
# Mock the external API call -- tests should not depend on network
# access or a real API key.
# ---------------------------------------------------------------------
 
def test_get_weather_returns_expected_shape(monkeypatch):
    monkeypatch.setenv("WEATHER_API_KEY", "test-key")

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "main": {"temp": 71.8},
                "weather": [{"description": "partly cloudy"}],
            }

    monkeypatch.setattr("requests.get", lambda *a, **k: FakeResponse())

    result = weather.get_weather(44.5646, -123.2620)
    assert result == {"temp_f": 72, "condition": "Partly cloudy"}


def test_get_weather_raises_without_api_key(monkeypatch):
    monkeypatch.delenv("WEATHER_API_KEY", raising=False)

    with pytest.raises(Exception):
        weather.get_weather(44.5646, -123.2620)
 
 
def test_get_weather_raises_on_api_failure(monkeypatch):
    monkeypatch.setenv("WEATHER_API_KEY", "test-key")

    class FailingResponse:
        def raise_for_status(self):
            raise Exception("simulated HTTP failure")

    monkeypatch.setattr("requests.get", lambda *a, **k: FailingResponse())

    with pytest.raises(Exception):
        weather.get_weather(44.5646, -123.2620)
 
 
# ---------------------------------------------------------------------
# Air quality source (sources/air_quality.py)
# Owner: Kelli
# Mock the external API call -- tests should not depend on network
# access or a real API key.
# ---------------------------------------------------------------------
 
def test_get_air_quality_returns_expected_shape(monkeypatch):
    # TODO: mock the HTTP call inside get_air_quality() and assert the
    # returned dict has the documented keys (aqi, category, ...).
    pass
 
 
def test_get_air_quality_raises_on_api_failure(monkeypatch):
    # TODO: mock the HTTP call to raise/return an error status and
    # assert get_air_quality() raises rather than silently failing.
    pass
 
 
# ---------------------------------------------------------------------
# Daylight source (sources/daylight.py)
# Owner: Samantha Brown
# Mock the external API call -- tests should not depend on network
# access or a real API key.
# ---------------------------------------------------------------------
 
def test_get_daylight_returns_expected_shape(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "results": {
                    "sunrise": "2026-08-09T13:12:00+00:00",
                    "sunset": "2026-08-10T03:41:00+00:00",
                },
                "status": "OK",
            }

    monkeypatch.setattr("requests.get", lambda *a, **k: FakeResponse())

    result = daylight.get_daylight(44.5646, -123.2620)

    assert result["sunrise"] == "2026-08-09T13:12:00Z"
    assert result["sunset"] == "2026-08-10T03:41:00Z"
    assert "is_daytime" in result
 

def test_get_daylight_raises_when_provider_reports_error_status(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"status" : "INVALID_REQUEST"}

    monkeypatch.setattr("requests.get", lambda *a, **k: FakeResponse())

    with pytest.raises(Exception):
        daylight.get_daylight(44.5646, -123.2620)

 
def test_get_daylight_raises_on_api_failure(monkeypatch):
    class FailingResponse:
        def raise_for_status(self):
            raise Exception("simulated HTTP failure")

    monkeypatch.setattr("requests.get", lambda *a, **k: FailingResponse())

    with pytest.raises(Exception):
        daylight.get_daylight(44.5646, -123.2620)