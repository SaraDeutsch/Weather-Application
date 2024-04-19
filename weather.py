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

# this function finds the latitude and longitude for the city and state inputed by the user. 
def get_lat_and_long(city_name, state_code, country_code, API_key):
    web_info = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()
    data_dict = web_info[0]
    lat, long = data_dict.get('lat'), data_dict.get('lon')
    return lat, long

# this function finds the weather given a latitude and longitude
def get_current_weather(latitude, longitude, api_key):
    weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial').json()
    # finds the main weather forecast
    main = weather.get('weather')[0].get('main')
    # finds the description of that forecase 
    description = weather.get('weather')[0].get('description')
    icon = ""
    icons_csv_path = '/workspaces/Weather-Application/templates/icons.csv'
    # iterates through the csv that matches the description to find the appropriate icon's image source
    with open(icons_csv_path) as csv_file:
        icons = csv.DictReader(csv_file)
        for item in icons:
            if item['weather'] == description:
                icon = item[' image source']
    temperature =int(weather.get('main').get('temp'))
    data = WeatherData(main, description, icon, temperature)
    return data

def main(city, state, country):
    lat, lon = get_lat_and_long(city, state, country, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data

if __name__ == "__main__":
    lat, lon = get_lat_and_long('Atlanta', 'GA', 'US', api_key)
    print(lat, lon)
    print(get_current_weather(lat, lon, api_key))