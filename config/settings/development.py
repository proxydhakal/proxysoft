"""
Local development settings. Uses SQLite. Loaded when DJANGO_ENV != production.
"""
import os
from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*"]

# SQLite for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Static/Media roots for dev
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Email: console by default; set EMAIL_BACKEND + SMTP in .env to test real delivery locally
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
if EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
    EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "true").lower() in ("1", "true", "yes")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

# Disable WhiteNoise compression in dev for easier debugging (optional)
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
