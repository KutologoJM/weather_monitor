"""
URL configuration for weather_monitor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from health_check.views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f"health/{settings.HEALTH_CHECK_TOKEN}/",
         HealthCheckView.as_view(
        checks=[  # optional, default is all but 3rd party checks
            "health_check.Cache",
            "health_check.Database",
            "health_check.Disk",
            "health_check.Mail",
            (
                "health_check.Memory",
                {  # tuple with options
                    "min_gibibytes_available": 0.1,  # 0.1 GiB (~100 MiB)
                    "max_memory_usage_percent": 80.0,
                },
            ),
            "health_check.Storage",
            # 3rd party checks
            # "health_check.contrib.celery.Ping",
            # "health_check.contrib.redis.Redis",
        ],
        use_threading=True,  # optional, default is True
        warnings_as_errors=True,  # optional, default is True
    ), name='health_check'),
    # path('accounts/', include('accounts.urls'))
    path("weather/", include("weather.urls"))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path(
                          "__debug__/", include(debug_toolbar.urls)
                      ),  # This registers the 'djdt' namespace
                      path("__reload__/", include("django_browser_reload.urls")),
                  ] + urlpatterns
