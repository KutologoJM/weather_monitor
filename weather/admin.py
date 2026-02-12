from django.contrib import admin

from .models import CurrentWeather, MinutelyWeather, HourlyWeather, DailyWeather, Alert


@admin.register(CurrentWeather)
class CurrentWeatherAdmin(admin.ModelAdmin):
    list_display = (
        'dt',
        'pressure',
        'humidity',
        'dew_point',
        'clouds',
        'uvi',
        'visibility',
        'wind_speed',
        'wind_gust',
        'wind_deg',
        'rain',
        'snow',
        'weather_id',
        'weather_main',
        'weather_description',
        'weather_icon',
        'weather_icon_image_url',
        'sunrise',
        'sunset',
        'temp',
        'feels_like',
    )
    list_filter = ('sunrise', 'sunset')


@admin.register(MinutelyWeather)
class MinutelyWeatherAdmin(admin.ModelAdmin):
    list_display = ('dt', 'datetime', 'precipitation', 'expire_at')
    list_filter = ('datetime', 'expire_at')


@admin.register(HourlyWeather)
class HourlyWeatherAdmin(admin.ModelAdmin):
    list_display = (
        'dt',
        'pressure',
        'humidity',
        'dew_point',
        'clouds',
        'uvi',
        'visibility',
        'wind_speed',
        'wind_gust',
        'wind_deg',
        'rain',
        'snow',
        'weather_id',
        'weather_main',
        'weather_description',
        'weather_icon',
        'weather_icon_image_url',
        'temp',
        'feels_like',
        'pop',
    )


@admin.register(DailyWeather)
class DailyWeatherAdmin(admin.ModelAdmin):
    list_display = (
        'dt',
        'pressure',
        'humidity',
        'dew_point',
        'clouds',
        'uvi',
        'wind_speed',
        'wind_gust',
        'wind_deg',
        'rain',
        'snow',
        'weather_id',
        'weather_main',
        'weather_description',
        'weather_icon',
        'weather_icon_image_url',
        'sunrise',
        'sunset',
        'moonrise',
        'moonset',
        'summary',
        'moon_phase',
        'pop',
        'temp_morn',
        'temp_day',
        'temp_eve',
        'temp_night',
        'temp_min',
        'temp_max',
        'feels_like_morn',
        'feels_like_day',
        'feels_like_eve',
        'feels_like_night',
    )
    list_filter = ('sunrise', 'sunset', 'moonrise', 'moonset')


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'sender_name',
        'event',
        'start',
        'end',
        'description',
        'tags',
    )
    list_filter = ('timestamp', 'start', 'end')
