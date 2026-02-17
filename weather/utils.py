def init_django_environment():
    import os
    import django
    from dotenv import load_dotenv

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_monitor.settings.dev")
    django.setup()
    load_dotenv()


def degrees_to_cardinal(degrees: float) -> str:
    """
    Converts degrees to cardinal directions using the cardinal_directions_mapping list.
    :param degrees: Degrees in decimal degrees
    :type degrees: float
    :return: Cardinal direction in the form 'N', 'SE', 'ENE', 'SSE', etc.
    :rtype: str

    Docs: https://openweathermap.org/faq#weather-related-symbols
    """
    degrees = float(degrees)
    cardinal_directions_mapping = [
        {"Cardinal Direction": "N", "Min Range": 348.75, "Max Range": 11.25},
        {"Cardinal Direction": "NNE", "Min Range": 11.25, "Max Range": 33.75},
        {"Cardinal Direction": "NE", "Min Range": 33.75, "Max Range": 56.25},
        {"Cardinal Direction": "ENE", "Min Range": 56.25, "Max Range": 78.75},
        {"Cardinal Direction": "E", "Min Range": 78.75, "Max Range": 101.25},
        {"Cardinal Direction": "ESE", "Min Range": 101.25, "Max Range": 123.75},
        {"Cardinal Direction": "SE", "Min Range": 123.75, "Max Range": 146.25},
        {"Cardinal Direction": "SSE", "Min Range": 146.25, "Max Range": 168.75},
        {"Cardinal Direction": "S", "Min Range": 168.75, "Max Range": 191.25},
        {"Cardinal Direction": "SSW", "Min Range": 191.25, "Max Range": 213.75},
        {"Cardinal Direction": "SW", "Min Range": 213.75, "Max Range": 236.25},
        {"Cardinal Direction": "WSW", "Min Range": 236.25, "Max Range": 258.75},
        {"Cardinal Direction": "W", "Min Range": 258.75, "Max Range": 281.25},
        {"Cardinal Direction": "WNW", "Min Range": 281.25, "Max Range": 303.75},
        {"Cardinal Direction": "NW", "Min Range": 303.75, "Max Range": 326.25},
        {"Cardinal Direction": "NNW", "Min Range": 326.25, "Max Range": 348.75},
    ]

    if not 0 <= degrees <= 360:
        raise ValueError("Degrees must be between 0 and 360 degrees")

    for mapping in cardinal_directions_mapping:
        min_range = mapping["Min Range"]
        max_range = mapping["Max Range"]

        if 348.75 < degrees or degrees < 11.25:
            return mapping["Cardinal Direction"]
        elif min_range <= degrees <= max_range:
            return mapping["Cardinal Direction"]
    raise ValueError("No cardinal direction found. Check mapping ranges.")
