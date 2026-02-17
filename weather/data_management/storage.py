import os

from weather.utils import init_django_environment

init_django_environment()

from creation import WeatherData
from weather.models import (
    CurrentWeather,
    MinutelyWeather,
    HourlyWeather,
    DailyWeather,
    Alert,
)

lat, lon = os.environ.get("LATITUDE"), os.environ.get("LONGITUDE")
if lat is None or lon is None:
    raise SystemExit(
        f"Latitude and longitude must be provided in environment variables."
    )


class WeatherStorage:

    def __init__(self):
        self.weather = WeatherData(lat, lon)
        self.current_weather = self.weather.get_current_weather()
        self.minutely_weather = self.weather.get_minutely_weather()
        self.hourly_weather = self.weather.get_hourly_weather()
        self.daily_weather = self.weather.get_daily_weather()
        self.weather_alerts = self.weather.get_weather_alert()

    def populate_current_weather(self):
        current_weather = self.current_weather
        dt = current_weather["dt"]
        obj, created = CurrentWeather.objects.get_or_create(
            dt=dt,
            defaults={
                "dt": dt,
                "pressure": current_weather["pressure"],
                "humidity": current_weather["humidity"],
                "dew_point": current_weather["dew_point"],
                "clouds": current_weather["clouds"],
                "uvi": current_weather["uvi"],
                "visibility": current_weather["visibility"],
                "wind_speed": current_weather["wind_speed"],
                "wind_gust": current_weather["wind_gust"],
                "wind_deg": current_weather["wind_deg"],
                "rain": current_weather["rain"],
                "snow": current_weather["snow"],
                "weather_id": current_weather["weather_id"],
                "weather_main": current_weather["weather_main"],
                "weather_description": current_weather["weather_description"],
                "weather_icon": current_weather["weather_icon"],
                "weather_icon_image_url": current_weather["weather_icon_image_url"],
                "sunrise": current_weather["sunrise"],
                "sunset": current_weather["sunset"],
                "temp": current_weather["temp"],
                "feels_like": current_weather["feels_like"],
            },
        )
        if created:
            return {"Success": f"Successfully populated current weather for dt:{dt}."}
        else:
            return {"Error": f"Failed to populate current weather for dt:{dt}."}

    def populate_minutely_weather(self):
        minutely_weather = self.minutely_weather
        dt = minutely_weather[
            "dt"
        ]  # todo save to redis instead of db / or create a bulk storage model
        obj, created = MinutelyWeather.objects.get_or_create(dt=dt, defaults={})
        if created:  # todo change to support multiple if going the model route
            return {"Success": f"Successfully populated minutely weather for dt:{dt}."}
        else:
            return {"Error": f"Failed to populate minutely weather for dt:{dt}."}

    def populate_hourly_weather(self):
        hourly_weather_list = self.hourly_weather
        for hourly_weather in hourly_weather_list:
            dt = hourly_weather["dt"]
            obj, created = HourlyWeather.objects.get_or_create(
                dt=dt,
                defaults={
                    "dt": dt,
                    "pressure": hourly_weather["pressure"],
                    "humidity": hourly_weather["humidity"],
                    "dew_point": hourly_weather["dew_point"],
                    "clouds": hourly_weather["clouds"],
                    "uvi": hourly_weather["uvi"],
                    "visibility": hourly_weather["visibility"],
                    "wind_speed": hourly_weather["wind_speed"],
                    "wind_gust": hourly_weather["wind_gust"],
                    "wind_deg": hourly_weather["wind_deg"],
                    "rain": hourly_weather["rain"],
                    "snow": hourly_weather["snow"],
                    "weather_id": hourly_weather["weather_id"],
                    "weather_main": hourly_weather["weather_main"],
                    "weather_description": hourly_weather["weather_description"],
                    "weather_icon": hourly_weather["weather_icon"],
                    "weather_icon_image_url": hourly_weather["weather_icon_image_url"],
                    "temp": hourly_weather["temp"],
                    "feels_like": hourly_weather["feels_like"],
                    "pop": hourly_weather["pop"],
                },
            )
            if created:
                print(f"Success: Successfully populated hourly weather for dt:{dt}.")
            else:
                print(f"Error: Failed to populate hourly weather for dt:{dt}.")
        return {"Processing Complete"}

    def populate_daily_weather(self):
        daily_weather_list = self.daily_weather
        for daily_weather in daily_weather_list:
            dt = daily_weather["dt"]
            obj, created = DailyWeather.objects.get_or_create(
                dt=dt,
                defaults={
                    "dt": dt,
                    "pressure": daily_weather["pressure"],
                    "humidity": daily_weather["humidity"],
                    "dew_point": daily_weather["dew_point"],
                    "clouds": daily_weather["clouds"],
                    "uvi": daily_weather["uvi"],
                    "wind_speed": daily_weather["wind_speed"],
                    "wind_gust": daily_weather["wind_gust"],
                    "wind_deg": daily_weather["wind_deg"],
                    "rain": daily_weather["rain"],
                    "snow": daily_weather["snow"],
                    "weather_id": daily_weather["weather_id"],
                    "weather_main": daily_weather["weather_main"],
                    "weather_description": daily_weather["weather_description"],
                    "weather_icon": daily_weather["weather_icon"],
                    "weather_icon_image_url": daily_weather["weather_icon_image_url"],
                    "sunrise": daily_weather["sunrise"],
                    "sunset": daily_weather["sunset"],
                    "moonrise": daily_weather["moonrise"],
                    "moonset": daily_weather["moonset"],
                    "summary": daily_weather["summary"],
                    "moon_phase": daily_weather["moon_phase"],
                    "pop": daily_weather["pop"],
                    "temp_morn": daily_weather["temp_morn"],
                    "temp_day": daily_weather["temp_day"],
                    "temp_eve": daily_weather["temp_eve"],
                    "temp_night": daily_weather["temp_night"],
                    "temp_min": daily_weather["temp_min"],
                    "temp_max": daily_weather["temp_max"],
                    "feels_like_morn": daily_weather["feels_like_morn"],
                    "feels_like_day": daily_weather["feels_like_day"],
                    "feels_like_eve": daily_weather["feels_like_eve"],
                    "feels_like_night": daily_weather["feels_like_night"],
                },
            )
            if created:
                print(f"Success: Successfully populated daily weather for dt:{dt}.")
            else:
                print(f"Error: Failed to populate daily weather for dt:{dt}.")
        return {"Processing Complete"}

    def populate_weather_alerts(self):
        weather_alerts = self.weather_alerts
        timestamp = weather_alerts["timestamp"]
        obj, created = Alert.objects.get_or_create(
            timestamp=timestamp,
            defaults={
                "timestamp": timestamp,
                "sender_name": weather_alerts["sender_name"],
                "event": weather_alerts["event"],
                "start": weather_alerts["start"],
                "end": weather_alerts["end"],
                "description": weather_alerts["description"],
                "tags": weather_alerts["tags"],
            },
        )
        if created:
            return {
                "Success": f"Successfully populated weather alert for timestamp:{timestamp}."
            }
        else:
            return {
                "Error": f"Failed to populate weather alert for timestamp:{timestamp}."
            }


storage = WeatherStorage()


def main():
    print(storage.populate_daily_weather())
    print(storage.populate_current_weather())
    print(storage.populate_hourly_weather())


if __name__ == "__main__":
    main()
