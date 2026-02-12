import os
import requests
from time import sleep
from datetime import datetime, UTC
from weather.utils import init_django_environment

init_django_environment()


lat, lon = os.environ.get("LATITUDE"), os.environ.get("LONGITUDE")
if lat is None or lon is None:
    raise SystemExit(
        f"Latitude and longitude must be provided in environment variables."
    )


def extract_weather_section(weather_dict):
    icon_code = weather_dict["weather"][0]["icon"]
    weather_icon_image_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    weather_id = weather_dict["weather"][0]["id"]
    weather_main = weather_dict["weather"][0]["main"]
    weather_description = weather_dict["weather"][0]["description"]
    weather_icon = weather_dict["weather"][0]["icon"]

    weather_data = {
        "weather_id": weather_id,
        "weather_main": weather_main,
        "weather_description": weather_description,
        "weather_icon": weather_icon,
        "weather_icon_image_url": weather_icon_image_url,
    }

    return weather_data


class WeatherData:

    def __init__(self, latitude: str, longitude: str):
        self.latitude: str = latitude
        self.longitude: str = longitude
        self.weather_data = self.get_weather_data()

    def get_weather_data(self):

        api_key: str = os.getenv("API_KEY")
        exclusion: str = ""
        endpoint = f"https://api.openweathermap.org/data/3.0/onecall?lat={self.latitude}&lon={self.longitude}&exclude={exclusion}&appid={api_key}&units=metric&lang=en"
        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                raw_weather_data = requests.get(endpoint).json()
                return dict(raw_weather_data)
            except requests.ConnectTimeout:
                retry_count += 1
                print(
                    f"Connection timed out, retrying ({retry_count}/{max_retries})..."
                )
                sleep(5 * 60)  # wait before retry

        # return error message if all retries fail
        return {"error": "Connection timed out"}

    def get_current_weather(self):
        """
        Extracts and formats current weather data and returns it as a dict
        :return: dictionary of current weather data

        """
        current_weather = self.weather_data["current"]
        weather_section = extract_weather_section(current_weather)
        current_weather["weather_id"] = weather_section["weather_id"]
        current_weather["weather_main"] = weather_section["weather_main"]
        current_weather["weather_description"] = weather_section["weather_description"]
        current_weather["weather_icon"] = weather_section["weather_icon"]
        current_weather["weather_icon_image_url"] = weather_section[
            "weather_icon_image_url"
        ]

        current_weather["sunrise"] = datetime.fromtimestamp(
            current_weather["sunrise"], tz=UTC
        )
        current_weather["sunset"] = datetime.fromtimestamp(
            current_weather["sunset"], tz=UTC
        )

        try:
            current_weather["rain"] = current_weather["1h"]
        except KeyError:
            current_weather["rain"] = None
        try:
            current_weather["snow"] = current_weather["snow"]["1h"]
        except KeyError:
            current_weather["snow"] = None
        try:
            current_weather["wind_gust"]
        except KeyError:
            current_weather["wind_gust"] = None

        return current_weather

    def get_minutely_weather(self):
        minutely_data_raw = self.weather_data["minutely"]
        return minutely_data_raw

    def get_hourly_weather(self):
        """
        Extracts and formats hourly weather data and returns it as a list of dicts
        :return:
        """
        hourly_weather_raw = self.weather_data["hourly"]
        hourly_weather_list = []
        for hourly_weather in hourly_weather_raw:

            weather_section = extract_weather_section(hourly_weather)
            hourly_weather["weather_id"] = weather_section["weather_id"]
            hourly_weather["weather_main"] = weather_section["weather_main"]
            hourly_weather["weather_description"] = weather_section[
                "weather_description"
            ]
            hourly_weather["weather_icon"] = weather_section["weather_icon"]
            hourly_weather["weather_icon_image_url"] = weather_section[
                "weather_icon_image_url"
            ]

            try:
                hourly_weather["rain"] = hourly_weather["1h"]
            except KeyError:
                hourly_weather["rain"] = None
            try:
                hourly_weather["snow"] = hourly_weather["snow"]["1h"]
            except KeyError:
                hourly_weather["snow"] = None
            try:
                hourly_weather["wind_gust"]
            except KeyError:
                hourly_weather["wind_gust"] = None
            hourly_weather_list.append(hourly_weather)

        return hourly_weather_list

    def get_daily_weather(self):
        """
        Extracts and formats daily weather data and returns it as a list of dicts
        :return:
        """
        daily_weather_raw = self.weather_data["daily"]
        daily_weather_list = []
        for daily_weather in daily_weather_raw:

            daily_weather["sunrise"] = datetime.fromtimestamp(
                daily_weather["sunrise"], tz=UTC
            )
            daily_weather["sunset"] = datetime.fromtimestamp(
                daily_weather["sunset"], tz=UTC
            )
            daily_weather["moonrise"] = datetime.fromtimestamp(
                daily_weather["moonrise"], tz=UTC
            )
            daily_weather["moonset"] = datetime.fromtimestamp(
                daily_weather["moonset"], tz=UTC
            )

            # temperature
            daily_weather["temp_morn"] = daily_weather["temp"]["morn"]
            daily_weather["temp_day"] = daily_weather["temp"]["day"]
            daily_weather["temp_eve"] = daily_weather["temp"]["eve"]
            daily_weather["temp_night"] = daily_weather["temp"]["night"]
            daily_weather["temp_min"] = daily_weather["temp"]["min"]
            daily_weather["temp_max"] = daily_weather["temp"]["max"]
            daily_weather.pop("temp")

            # feels like
            daily_weather["feels_like_morn"] = daily_weather["feels_like"]["morn"]
            daily_weather["feels_like_day"] = daily_weather["feels_like"]["day"]
            daily_weather["feels_like_eve"] = daily_weather["feels_like"]["eve"]
            daily_weather["feels_like_night"] = daily_weather["feels_like"]["night"]
            daily_weather.pop("feels_like")

            weather_section = extract_weather_section(daily_weather)
            daily_weather["weather_id"] = weather_section["weather_id"]
            daily_weather["weather_main"] = weather_section["weather_main"]
            daily_weather["weather_description"] = weather_section[
                "weather_description"
            ]
            daily_weather["weather_icon"] = weather_section["weather_icon"]
            daily_weather["weather_icon_image_url"] = weather_section[
                "weather_icon_image_url"
            ]
            daily_weather.pop("weather")
            try:
                daily_weather["rain"] = daily_weather["1h"]
            except KeyError:
                daily_weather["rain"] = None
            try:
                daily_weather["snow"] = daily_weather["snow"]["1h"]
            except KeyError:
                daily_weather["snow"] = None
            try:
                daily_weather["wind_gust"]
            except KeyError:
                daily_weather["wind_gust"] = None

            daily_weather_list.append(daily_weather)
        return daily_weather_list

    def get_weather_alert(self):
        pass
