"""
Django base settings. Environment-specific settings override in development.py / production.py.
"""
import os
from pathlib import Path

import environ

# Build paths (config/settings/base.py -> config -> project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root (proxy-soft)

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    SECRET_KEY=(str, "change-me-in-production"),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY", default="dev-secret-key-change-in-production")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
ADMIN_URL = env("ADMIN_URL", default="admin/")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "apps.accounts",
    "apps.core",
    "ckeditor",
    "ckeditor_uploader",
    "apps.pages",
    "apps.blog",
]
LOGIN_URL = "/iamadmin/login/"
LOGIN_REDIRECT_URL = "/iamadmin/"
LOGOUT_REDIRECT_URL = "/iamadmin/login/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_config",
            ],
        },
    },
]

# Auth
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and media (paths; STATIC_ROOT/MEDIA_ROOT set per env)
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")] if os.path.exists(os.path.join(BASE_DIR, "static")) and os.path.isdir(os.path.join(BASE_DIR, "static")) else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = 1

# Security (production overrides these further)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

# CKEditor (rich text for pages & blog)
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 420,
        "width": "100%",
        "toolbar_Full": [
            ["Styles", "Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker", "Undo", "Redo"],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Table", "HorizontalRule"],
            ["TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
            ["Source"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock"],
            ["NumberedList", "BulletedList"],
            ["Indent", "Outdent"],
            ["Maximize"],
        ],
    },
}
