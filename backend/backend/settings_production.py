# backend/backend/settings_production.py
import os
from pathlib import Path
import dj_database_url

# Import everything from your base settings file
# (keep original settings.py as the local/dev configuration)
from .settings import *  # noqa: F401,F403

# ---------- Basic production overrides ----------
DEBUG = False

# SECRET KEY from env (must be set on Render)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

# ALLOWED_HOSTS: comma-separated env var, fallback to empty list
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]

# CORS origins: comma-separated env var (no trailing slashes)
CORS_ALLOWED_ORIGINS = [h.strip() for h in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if h.strip()]

# CSRF trusted origins (use same hosts as ALLOWED_HOSTS, prefixed with https:// when needed)
CSRF_TRUSTED_ORIGINS = [f"https://{h}" if not h.startswith("http") else h for h in ALLOWED_HOSTS]

# ---------- Database: use dj_database_url to parse DATABASE_URL ----------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# ---------- Static files & whitenoise ----------
# ensure STATIC_ROOT exists in base settings or set here:
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / "staticfiles"

# Add whitenoise middleware (insert after SecurityMiddleware if not already present)
MIDDLEWARE = list(MIDDLEWARE)  # copy to be safe
if "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
    try:
        idx = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1
    except ValueError:
        idx = 0
    MIDDLEWARE.insert(idx, "whitenoise.middleware.WhiteNoiseMiddleware")

# Use whitenoise static storage for compressed static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------- Security hardening (recommended) ----------
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
