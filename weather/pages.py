from flask import Blueprint, render_template, request
import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim
from .models import db, City

bp = Blueprint("pages", __name__)


@bp.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city_name = request.form.get('city')
        user_id = 1
        # Сохраняем или обновляем информацию о городе в БД
        city = City.query.filter_by(name=city_name, user_id=user_id).first()
        if city:
            city.search_count += 1
        else:
            city = City(name=city_name, user_id=user_id, search_count=1)
            db.session.add(city)
        db.session.commit()

        # Запрос к API погоды
        response = get_weather(city_name)
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_wind_speed_10m = current.Variables(2).Value()
        weather_data = {
            'city': city_name,
            'temperature': f'{current_temperature_2m:.1f}',
            'apparent_temperature': f'{current_apparent_temperature:.1f}',
            'wind_speed_10m': f'{current_wind_speed_10m:.1f}'
        }
        return render_template('home.html', weather=weather_data)
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
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": ["temperature_2m", "apparent_temperature", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
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
    return response
