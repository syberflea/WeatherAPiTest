from flask import Blueprint, render_template, request
import requests
from models import db, City


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form.get('city')
        user_id = 1  # Для простоты используем фиксированный user_id

        # Сохраняем или обновляем информацию о городе
        city = City.query.filter_by(name=city_name, user_id=user_id).first()
        if city:
            city.search_count += 1
        else:
            city = City(name=city_name, user_id=user_id, search_count=1)
            db.session.add(city)
        db.session.commit()

        # Запрос к API погоды
        weather_data = get_weather(city_name)
        return render_template('index.html', weather=weather_data)

    return render_template('index.html')


def get_weather(city):
    url = f"https://api.open-meteo.com/v1/forecast?latitude=35.6895&lon39.6917&current_weather=true"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}
