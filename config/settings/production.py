"""
Production settings. Uses MySQL. Loaded when DJANGO_ENV=production.
"""
import os
from .base import *  # noqa: F401, F403

DEBUG = env.bool("DEBUG", False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# MySQL for production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

STATIC_ROOT = env("STATIC_ROOT", default=os.path.join(BASE_DIR, "staticfiles"))
MEDIA_ROOT = env("MEDIA_ROOT", default=os.path.join(BASE_DIR, "media"))

# Security
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Caching (optional - use Redis or Memcached in production)
# CACHES = { ... }

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log"),
        },
    },
    "root": {"handlers": ["file"], "level": "ERROR"},
}
