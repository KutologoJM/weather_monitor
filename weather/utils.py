def init_django_environment():
    import os
    import django
    from dotenv import load_dotenv

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_monitor.settings.dev")
    django.setup()
    load_dotenv()
