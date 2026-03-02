"""
Level 6 - Exercise 01: Weather CLI Tool
=========================================

Difficulty: 3/5 stars
Estimated time: 25 minutes

Build a command-line weather tool that can fetch data from the
OpenWeatherMap API.  Includes a full DEMO MODE with mock data so the
script works without an API key.

Features
--------
- Fetch current weather by city name.
- Display temperature, humidity, wind, and description.
- Supports Celsius / Fahrenheit.
- Demo mode with realistic mock data (no network required).

Usage:
    python3 01-weather-cli.py London
    python3 01-weather-cli.py "New York" --units imperial
    python3 01-weather-cli.py Tokyo --demo          # uses mock data

Expected output (demo mode):
-----------------------------
    Weather for London, GB
    -----------------------
    Description : scattered clouds
    Temperature : 15.2 C
    Feels like  : 13.8 C
    Humidity    : 72%
    Wind        : 4.1 m/s
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError


# ---------------------------------------------------------------------------
# Mock data for demo mode (no API key required)
# ---------------------------------------------------------------------------
MOCK_DATA = {
    "london": {
        "name": "London",
        "sys": {"country": "GB"},
        "weather": [{"description": "scattered clouds", "icon": "03d"}],
        "main": {
            "temp": 15.2,
            "feels_like": 13.8,
            "temp_min": 12.0,
            "temp_max": 17.5,
            "humidity": 72,
            "pressure": 1013,
        },
        "wind": {"speed": 4.1, "deg": 230},
        "visibility": 10000,
    },
    "new york": {
        "name": "New York",
        "sys": {"country": "US"},
        "weather": [{"description": "clear sky", "icon": "01d"}],
        "main": {
            "temp": 72.5,
            "feels_like": 70.1,
            "temp_min": 68.0,
            "temp_max": 76.0,
            "humidity": 45,
            "pressure": 1020,
        },
        "wind": {"speed": 8.2, "deg": 180},
        "visibility": 16093,
    },
    "tokyo": {
        "name": "Tokyo",
        "sys": {"country": "JP"},
        "weather": [{"description": "light rain", "icon": "10d"}],
        "main": {
            "temp": 22.0,
            "feels_like": 23.5,
            "temp_min": 20.0,
            "temp_max": 24.0,
            "humidity": 88,
            "pressure": 1005,
        },
        "wind": {"speed": 2.5, "deg": 90},
        "visibility": 8000,
    },
    "paris": {
        "name": "Paris",
        "sys": {"country": "FR"},
        "weather": [{"description": "overcast clouds", "icon": "04d"}],
        "main": {
            "temp": 18.3,
            "feels_like": 17.0,
            "temp_min": 15.5,
            "temp_max": 20.1,
            "humidity": 65,
            "pressure": 1015,
        },
        "wind": {"speed": 3.6, "deg": 310},
        "visibility": 10000,
    },
}


# ---------------------------------------------------------------------------
# API Fetcher
# ---------------------------------------------------------------------------
def fetch_weather(city: str, api_key: str, units: str = "metric") -> dict:
    """Fetch current weather from OpenWeatherMap API.

    Parameters
    ----------
    city : str
        City name (e.g. "London", "New York").
    api_key : str
        Your OpenWeatherMap API key.
    units : str
        "metric" (Celsius) or "imperial" (Fahrenheit).

    Returns
    -------
    dict
        Parsed JSON response from the API.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    url = f"{base_url}?q={city}&appid={api_key}&units={units}"
    req = Request(url, headers={"User-Agent": "PythonWeatherCLI/1.0"})

    try:
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except URLError as exc:
        print(f"Error fetching weather: {exc}")
        sys.exit(1)


def fetch_weather_demo(city: str, units: str = "metric") -> dict:
    """Return mock weather data (no network call)."""
    key = city.lower().strip()
    if key in MOCK_DATA:
        return MOCK_DATA[key]
    # Fallback: generate generic data
    return {
        "name": city.title(),
        "sys": {"country": "??"},
        "weather": [{"description": "partly cloudy", "icon": "02d"}],
        "main": {
            "temp": 20.0,
            "feels_like": 19.0,
            "temp_min": 17.0,
            "temp_max": 23.0,
            "humidity": 55,
            "pressure": 1012,
        },
        "wind": {"speed": 3.0, "deg": 0},
        "visibility": 10000,
    }


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
def display_weather(data: dict, units: str = "metric") -> None:
    """Pretty-print weather data to the console."""
    temp_unit = "C" if units == "metric" else "F"
    speed_unit = "m/s" if units == "metric" else "mph"

    city = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    weather = data.get("weather", [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})

    header = f"Weather for {city}, {country}"
    print(f"\n{header}")
    print("-" * len(header))
    print(f"  Description : {weather.get('description', 'N/A')}")
    print(f"  Temperature : {main.get('temp', 'N/A')} {temp_unit}")
    print(f"  Feels like  : {main.get('feels_like', 'N/A')} {temp_unit}")
    print(f"  Min / Max   : {main.get('temp_min', '?')} / {main.get('temp_max', '?')} {temp_unit}")
    print(f"  Humidity    : {main.get('humidity', 'N/A')}%")
    print(f"  Pressure    : {main.get('pressure', 'N/A')} hPa")
    print(f"  Wind        : {wind.get('speed', 'N/A')} {speed_unit}")
    visibility_km = (data.get("visibility", 0) or 0) / 1000
    print(f"  Visibility  : {visibility_km:.1f} km")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch and display current weather for a city."
    )
    parser.add_argument("city", help="City name (e.g. London, 'New York')")
    parser.add_argument(
        "--units",
        choices=["metric", "imperial"],
        default="metric",
        help="Temperature units (default: metric / Celsius)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="OpenWeatherMap API key (or set OWM_API_KEY env var)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Use mock data (no API key / network needed)",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.demo:
        print("[DEMO MODE] Using mock weather data.")
        data = fetch_weather_demo(args.city, args.units)
    else:
        import os
        api_key = args.api_key or os.environ.get("OWM_API_KEY")
        if not api_key:
            print("No API key provided. Falling back to DEMO MODE.")
            print("Set OWM_API_KEY env var or pass --api-key, or use --demo.\n")
            data = fetch_weather_demo(args.city, args.units)
        else:
            data = fetch_weather(args.city, api_key, args.units)

    display_weather(data, args.units)


# ===================================================================
# Demo / self-test
# ===================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        # No arguments -- run interactive demo
        print("No city provided. Running demo for multiple cities...\n")
        for city in ["London", "New York", "Tokyo", "Paris", "Berlin"]:
            data = fetch_weather_demo(city)
            display_weather(data, "metric")
    else:
        main()
