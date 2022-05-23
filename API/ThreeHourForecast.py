import requests
from datetime import datetime
from typing import List, Dict


class WeatherData(object):
    def __init__(self, city: str, date: str, temperature: float, feels_like: float,
                 humidity: int, wind_speed: float, description: str):
        self.city = city
        self.date = date
        self.temperature = temperature
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.description = description


class ThreeHourForecast(object):
    def __init__(self, country: str, city: str, api_key: str, units: str = 'metric', lang: str = 'pl', limit: int = 8):
        lat_lon_url: str = f"https://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid={api_key}"
        lat_lon: Dict = requests.get(lat_lon_url).json()
        forecast_url: str = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat_lon[0]['lat']}" \
                            f"&lon={lat_lon[0]['lon']}&appid={api_key}&units={units}&lang={lang}&cnt={limit}"
        data: Dict = requests.get(forecast_url).json()
        self.list_of_weather_data: List[Dict] = data["list"]
        self.parsed_data: List[WeatherData] = [WeatherData(city,
                                               datetime.utcfromtimestamp(x["dt"] + 7200).strftime('%d-%m-%Yr. %H:%M:%S'),
                                               x["main"]["temp"],
                                               x["main"]["feels_like"],
                                               x["main"]["humidity"],
                                               x["wind"]["speed"],
                                               x["weather"][0]["description"]) for x in self.list_of_weather_data]