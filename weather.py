import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import csv

load_dotenv()
api_key = os.getenv('api_code')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int

def get_lat_and_long(city_name, state_code, country_code, API_key):
    web_info = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()
    data_dict = web_info[0]
    lat, long = data_dict.get('lat'), data_dict.get('lon')
    return lat, long

def get_current_weather(latitude, longitude, api_key):
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial').json()
    main = weather.get('weather')[0].get('main')
    description = weather.get('weather')[0].get('description')
    icon = ""
    with open('icons.csv') as csv_file:
        icons = csv.Reader(csv_file)
        for item in icons:
            if item[0] == description:
                icon = item[2]
                break
    temperature =int(weather.get('main').get('temp'))
    data = WeatherData(main, description, icon, temperature)
    return data
def main(city, state, country):
    lat, lon = get_lat_and_long(city, state, country, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data
# if __name__ == "__main__":
#     lat, lon = get_lat_and_long('Toronto', 'ON', 'Canada', api_key)
#     # print(get_current_weather(lat, lon, api_key))