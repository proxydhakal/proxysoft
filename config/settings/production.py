"""
Production settings. Uses MySQL. Loaded when DJANGO_ENV=production.

Run deploy checks (on the server or with prod .env loaded)::

  DJANGO_ENV=production python manage.py check --deploy
"""
import os
from .base import *  # noqa: F401, F403

DEBUG = env.bool("DEBUG", False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# HTTPS sites behind a reverse proxy: set e.g. CSRF_TRUSTED_ORIGINS=https://yourdomain.com
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

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

# Email (SMTP)
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER or "noreply@localhost")
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# Security
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Third-party advisory; switching to CKEditor 5 is a larger change.
SILENCED_SYSTEM_CHECKS = ["ckeditor.W001"]

# Caching (optional - use Redis or Memcached in production)
# CACHES = { ... }

# Logging (ensure log directory exists so Django can start)
_LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(_LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(_LOG_DIR, "django.log"),
        },
    },
    "root": {"handlers": ["file"], "level": "ERROR"},
}
