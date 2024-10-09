# WeatherAPITest — тестовое задание для hh.ru. 

## Описание проекта
Сделать web приложение, оно же сайт, где пользователь вводит название города, и получает прогноз погоды в этом городе на ближайшее время.
 - Вывод данных (прогноза погоды) должен быть в удобно читаемом формате. 
 - Веб фреймворк можно использовать любой.
 - api для погоды:* https://open-meteo.com/ *(можно использовать какое-нибудь другое, если вам удобнее)*

Будет плюсом если:

- написаны тесты
- всё это помещено в докер контейнер
- сделаны автодополнение (подсказки) при вводе города
- при повторном посещении сайта будет предложено посмотреть погоду в городе, в котором пользователь уже смотрел ранее
- будет сохраняться история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город

## Технологии
 - Python 3.10.11
 - Flask 3.0.3
 - Docker


## Локальное развертывание проекта
1. Клонируйте репозиторий [WeatherAPiTest](git@github.com:syberflea/WeatherAPiTest.git).
2. В каталоге с проектом создайте и активируйте виртуальное окружение: `python3 -m venv venv && source venv/bin/activate`
3. Установите зависимости: `pip install -r requirements.txt`.  

### Создание Docker-образов
1. Замените username на ваш логин на DockerHub:
```
docker build -t username/weatherapi .
```
2. Загрузите образы на DockerHub:
```
docker push username/weatherapi
```

## Установка проекта на сервер

1. Подключитесь к удаленному серверу

```ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера ```

2. Создайте на сервере директорию weather_api_test

`mkdir weather_api_test`

3. Установка docker compose на сервер:
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```

Скопируйте файл docker-compose.production.yml:
```
scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/weather_api_test/docker-compose.production.yml
```

4. Запустите docker compose в режиме демона:

`sudo docker compose -f docker-compose.production.yml up -d`

(с) Евгений Андронов, 2024
