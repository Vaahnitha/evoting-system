# backend/backend/settings_production.py
import os
from pathlib import Path
import dj_database_url

# Import base (dev) settings
from .settings import *  # noqa: F401,F403

# Production overrides
DEBUG = False

# Secret key from env
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

# Hosts and CORS from env (comma-separated)
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]
CORS_ALLOWED_ORIGINS = [h.strip() for h in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if h.strip()]

# CSRF trusted origins: prefix with https:// when needed
CSRF_TRUSTED_ORIGINS = [f"https://{h}" if not h.startswith("http") else h for h in ALLOWED_HOSTS]

# Database (parse DATABASE_URL)
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# Static files
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / "staticfiles"

# Add whitenoise if not present
MIDDLEWARE = list(MIDDLEWARE)
if "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
    try:
        idx = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1
    except ValueError:
        idx = 0
    MIDDLEWARE.insert(idx, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Security recommended headers
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
