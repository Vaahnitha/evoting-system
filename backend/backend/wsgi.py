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
        # Respect externally provided settings module (e.g., production)
        settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'backend.settings')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        application = get_wsgi_application()
        try:
            call_command('migrate', interactive=False, run_syncdb=True)
        except Exception:
            # Avoid crashing dyno on transient errors
            pass
        try:
            # Optional one-time admin seeding controlled via env vars
            if os.getenv("SEED_ADMIN", "false").lower() == "true":
                from django.contrib.auth import get_user_model
                User = get_user_model()
                admin_username = os.getenv("ADMIN_USERNAME", "admin")
                admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
                admin_password = os.getenv("ADMIN_PASSWORD")
                if admin_password:
                    if not User.objects.filter(username=admin_username).exists():
                        User.objects.create_superuser(
                            username=admin_username,
                            email=admin_email,
                            password=admin_password,
                        )
                        print(f"Created admin user: {admin_username}")
                    else:
                        print(f"Admin user {admin_username} already exists")
                else:
                    print("ADMIN_PASSWORD not set, skipping admin user creation")
        except Exception as e:
            # Log seeding errors but don't block boot
            print(f"Admin seeding error: {e}")
            pass
        # Return the application after migrations
        # Fall through to final application assignment below
except Exception:
    # If importing management or calling migrate fails, continue normally
    pass

settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'backend.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()

