"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Attempt automatic migrations on startup (safe no-op if DB locked or not ready)
try:
    from django.core.management import call_command
    # Only attempt when explicitly enabled or when on Render
    if os.getenv("AUTO_MIGRATE", "true").lower() == "true" or os.getenv("RENDER"):
        # Defer execution until settings are loaded
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
        application = get_wsgi_application()
        try:
            call_command('migrate', interactive=False, run_syncdb=True)
        except Exception:
            # Avoid crashing dyno on transient errors
            pass
        # Return the application after migrations
        # Fall through to final application assignment below
except Exception:
    # If importing management or calling migrate fails, continue normally
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

