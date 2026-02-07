from datetime import timedelta
from datetime import datetime
from django.db import models


# Create your models here.

class StandardWeatherModel(models.Model):
    dt = models.BigIntegerField(primary_key=True, unique=True, help_text="Current time, Unix, UTC")
    pressure = models.IntegerField(help_text="Atmospheric pressure on the sea level. Units: hPa")
    humidity = models.FloatField(help_text="Humidity. Units: %")
    dew_point = models.FloatField(help_text="Dew point temperature. Units: Celsius")
    clouds = models.FloatField(help_text="Cloud cover. Units: %")
    uvi = models.FloatField(help_text="UV index")
    visibility = models.FloatField(help_text=" Average visibility. Units: m, Max value is 10 km")
    wind_speed = models.FloatField(help_text="Wind speed. Units: m/s")
    wind_gust = models.FloatField(null=True, help_text="Wind gust. Units: m/s")
    wind_deg = models.FloatField(help_text="Wind direction. Units: degrees(meteorological)")
    rain = models.FloatField(null=True, help_text="Precipitation. Units: mm/h")
    snow = models.FloatField(null=True, help_text="Snow. Units: mm/h")
    # https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
    weather_id = models.IntegerField(help_text="Weather ID code. E.g 201")
    weather_main = models.CharField(max_length=20, help_text=" Group of weather parameters (Rain, Snow etc.)")
    weather_description = models.CharField(max_length=50, help_text="Weather condition within the group ")
    weather_icon = models.CharField(max_length=3, help_text="Weather Icon code. E.g 04d")
    weather_icon_image_url = models.URLField()

    class Meta:
        abstract = True


class CurrentWeather(StandardWeatherModel):
    sunrise = models.DateTimeField(help_text="Sunrise time, Unix, UTC")
    sunset = models.DateTimeField(help_text="Sunset time, Unix, UTC")
    temp = models.FloatField(help_text="Current temperature. Units: Celsius")
    feels_like = models.FloatField(
        help_text="Temperature. This temperature parameter accounts for the human perception of weather Units: Celsius")

    class Meta:
        verbose_name = "Current Weather"
        verbose_name_plural = "Current Weather"

    def __str__(self):
        local_dt = datetime.fromtimestamp(self.dt)
        return f"Current Weather for {local_dt}"


class MinutelyWeather(models.Model):
    dt = models.BigIntegerField(primary_key=True, unique=True, help_text="Current time, Unix, UTC")
    datetime = models.DateTimeField(help_text="Time of the forecasted data, unix, UTC")
    precipitation = models.FloatField(help_text="Precipitation. Units: mm/h")
    expire_at = models.DateTimeField()

    class Meta:
        verbose_name = "Minutely Weather"
        verbose_name_plural = "Minutely Weather"

    def __str__(self):
        from datetime import datetime
        local_dt = datetime.fromtimestamp(self.dt)
        return f"Minutely Weather for {local_dt}"

    def save(self, *args, **kwargs):
        if not self.expire_at:
            # Automatically set expiration, e.g., 24 hours after creation
            self.expire_at = self.datetime + timedelta(hours=24)
        super().save(*args, **kwargs)


class HourlyWeather(StandardWeatherModel):
    temp = models.FloatField(help_text="Current temperature. Units: Celsius")
    feels_like = models.FloatField(
        help_text="Temperature. This temperature parameter accounts for the human perception of weather Units: Celsius")
    pop = models.IntegerField(
        help_text="Probability of precipitation. The values of the parameter vary between 0 and 1, where 0 is equal to 0%, 1 is equal to 100%")

    class Meta:
        verbose_name = "Hourly Weather"
        verbose_name_plural = "Hourly Weather"

    def __str__(self):
        local_dt = datetime.fromtimestamp(self.dt)
        return f"Hourly Weather for {local_dt}"


class DailyWeather(StandardWeatherModel):
    sunrise = models.DateTimeField(help_text="Sunrise time, Unix, UTC")
    sunset = models.DateTimeField(help_text="Sunset time, Unix, UTC")
    moonrise = models.DateTimeField(help_text="The time of when the moon rises for this day, Unix, UTC")
    moonset = models.DateTimeField(help_text="The time of when the moon sets for this day, Unix, UTC")
    summary = models.TextField(help_text="Human-readable description of the weather conditions for the day")
    moon_phase = models.FloatField(
        help_text="Moon phase. 0 and 1 are 'new moon', 0.25 is 'first quarter moon', 0.5 is 'full moon' and 0.75 is 'last quarter moon'. ")
    pop = models.IntegerField(
        help_text="Probability of precipitation. The values of the parameter vary between 0 and 1, where 0 is equal to 0%, 1 is equal to 100%")

    temp_morn = models.FloatField(help_text="Morning temperature. Units: Celsius")
    temp_day = models.FloatField(help_text="Day temperature. Units: Celsius")
    temp_eve = models.FloatField(help_text="Eve temperature. Units: Celsius")
    temp_night = models.FloatField(help_text="Night temperature. Units: Celsius")
    temp_min = models.FloatField(help_text="Min daily temperature. Units: Celsius")
    temp_max = models.FloatField(help_text="Max daily temperature. Units: Celsius")

    feels_like_morn = models.FloatField(help_text="Morning temperature. Units: Celsius")
    feels_like_day = models.FloatField(help_text="Day temperature. Units: Celsius")
    feels_like_eve = models.FloatField(help_text="Evening temperature. Units: Celsius")
    feels_like_night = models.FloatField(help_text="Night temperature. Units: Celsius")

    class Meta:
        verbose_name = "Daily Weather"
        verbose_name_plural = "Daily Weather"

    def __str__(self):
        local_dt = datetime.fromtimestamp(self.dt)
        return f"Current Weather for {local_dt}"


class Alert(models.Model):
    timestamp = models.DateTimeField(primary_key=True, unique=True, auto_now_add=True)
    sender_name = models.TextField(help_text="Name of the alert source")
    event = models.CharField(max_length=100, help_text="Alert event name")
    start = models.DateTimeField(help_text="Date and time of the start of the alert, Unix, UTC")
    end = models.DateTimeField(help_text="Date and time of the end of the alert, Unix, UTC")
    description = models.TextField(help_text="Description of the alert")
    tags = models.TextField(help_text="Type of severe weather")

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"

    def __str__(self):
        return f"Weather alert for {self.timestamp}"
