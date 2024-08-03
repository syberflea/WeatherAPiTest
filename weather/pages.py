from flask import Blueprint, render_template
import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim

bp = Blueprint("pages", __name__)


@bp.route("/")
def home():
    get_weather()
    return render_template("home.html")


@bp.route("/about")
def about():
    return "Hello, About!"


def get_weather(city=None):
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    geolocator = Nominatim(user_agent="weather-agent")
    location = geolocator.geocode(city)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "current": ["temperature_2m", "apparent_temperature", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    print(response)
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()
    current_wind_speed_10m = current.Variables(2).Value()

    print(f"Current time {current.Time()}")
    print(f"Current temperature_2m {current_temperature_2m}")
    print(f"Current apparent_temperature {current_apparent_temperature}")
    print(f"Current wind_speed_10m {current_wind_speed_10m}")
    # .json() if response.status_code == 200 else {}
    return response
