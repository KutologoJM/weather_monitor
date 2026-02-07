from django.contrib import admin
from weather.models import CurrentWeather, MinutelyWeather, HourlyWeather, DailyWeather, Alert

# Register your models here.
admin.site.register(CurrentWeather)
admin.site.register(MinutelyWeather)
admin.site.register(HourlyWeather)
admin.site.register(DailyWeather)
admin.site.register(Alert)
