# backend/backend/settings_production.py
import os
from pathlib import Path
from importlib import import_module
import dj_database_url
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import base (dev) settings
from .settings import *  # noqa: F401,F403

# Production overrides
# Allow overriding via env for local debugging when this settings module is selected
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Secret key from env
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

# Hosts and CORS from env (comma-separated) with safe fallbacks
_env_allowed_hosts = os.environ.get("ALLOWED_HOSTS")
if _env_allowed_hosts:
    ALLOWED_HOSTS = [h.strip() for h in _env_allowed_hosts.split(",") if h.strip()]
else:
    # Fall back to base settings or localhost to avoid runtime error when DEBUG=False
    ALLOWED_HOSTS = globals().get("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])  # type: ignore

_env_cors_origins = os.environ.get("CORS_ALLOWED_ORIGINS")
if _env_cors_origins:
    CORS_ALLOWED_ORIGINS = [h.strip() for h in _env_cors_origins.split(",") if h.strip()]
else:
    CORS_ALLOWED_ORIGINS = globals().get("CORS_ALLOWED_ORIGINS", [
        "http://localhost:3000",
        "https://evoting-system-rho.vercel.app",
        "https://evoting-system-a2tkfmhhp-vaahnithas-projects.vercel.app",
        "https://evoting-system-nvyxmh6r7-vaahnithas-projects.vercel.app",
    ])  # type: ignore

# Add wildcard support for Vercel domains
CORS_ALLOW_ALL_ORIGINS = False  # Keep this False for security
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://evoting-system-.*-vaahnithas-projects\.vercel\.app$",
    r"^https://evoting-system-rho\.vercel\.app$",
]

# CSRF trusted origins: prefix with https:// when needed
CSRF_TRUSTED_ORIGINS = [
    (f"https://{h}" if not h.startswith("http") else h)
    for h in ALLOWED_HOSTS
    if h not in ("localhost", "127.0.0.1")
] + ["https://evoting-system-rho.vercel.app", "https://evoting-system-a2tkfmhhp-vaahnithas-projects.vercel.app", "https://evoting-system-nvyxmh6r7-vaahnithas-projects.vercel.app"]

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

# Add whitenoise if installed
try:
    import_module("whitenoise.middleware")
    MIDDLEWARE = list(MIDDLEWARE)
    if "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
        try:
            idx = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1
        except ValueError:
            idx = 0
        MIDDLEWARE.insert(idx, "whitenoise.middleware.WhiteNoiseMiddleware")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
except ModuleNotFoundError:
    # Skip whitenoise configuration if not available
    pass

# Security recommended headers
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
