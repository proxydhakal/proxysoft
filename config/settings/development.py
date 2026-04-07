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

# Email (console for dev)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable WhiteNoise compression in dev for easier debugging (optional)
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
