# settings/dev.py
from .base import *  # noqa: F403

DEBUG = os.getenv("DEBUG_DEV")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

INTERNAL_IPS = [
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")

INSTALLED_APPS += ["debug_toolbar", "django_browser_reload", "django_watchfiles", ]  # noqa: F405

MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
MIDDLEWARE.insert(
    3, "django_browser_reload.middleware.BrowserReloadMiddleware"
)  # noqa: F405

DATABASES = {
    "default": dj_database_url.config(  # noqa: F405
        default=os.getenv("DATABASE_URL_DEV"),  # noqa: F405
        conn_max_age=600,
        ssl_require=True,
    )
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
