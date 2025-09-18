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
        
        # Optional one-time data import from local database
        try:
            print(f"IMPORT_LOCAL_DATA env var: {os.getenv('IMPORT_LOCAL_DATA', 'false')}")
            if os.getenv("IMPORT_LOCAL_DATA", "false").lower() == "true":
                from voting.models import Candidate, Vote
                from django.contrib.auth import get_user_model
                from django.db import transaction
                
                User = get_user_model()
                
                # Check if candidates exist (more specific check)
                candidate_count = Candidate.objects.count()
                print(f"Current candidate count: {candidate_count}")
                if candidate_count == 0:
                    print("Importing local data...")
                    
                    with transaction.atomic():
                        # Import candidates
                        candidates_data = [
                            {'id': 1, 'name': 'john doe', 'department': 'eng'},
                            {'id': 2, 'name': 'jane doe', 'department': 'hr'},
                            {'id': 3, 'name': 'alex b', 'department': 'pm'},
                            {'id': 4, 'name': 'cow', 'department': 'moo'},
                        ]
                        
                        for candidate_data in candidates_data:
                            candidate, created = Candidate.objects.get_or_create(
                                id=candidate_data['id'],
                                defaults={
                                    'name': candidate_data['name'],
                                    'department': candidate_data['department'],
                                }
                            )
                            if created:
                                print(f"Imported candidate: {candidate.name}")
                        
                        # Import users
                        users_data = [
                            {
                                'id': 1, 'username': 'Vaahnitha', 'email': 'vaahnithachowdary.ch@gmail.com',
                                'first_name': '', 'last_name': '', 'role': 'employee',
                                'is_staff': True, 'is_active': True,
                            },
                            {
                                'id': 7, 'username': 'employee1', 'email': '',
                                'first_name': '', 'last_name': '', 'role': 'employee',
                                'is_staff': False, 'is_active': True,
                            },
                            {
                                'id': 8, 'username': 'Admin', 'email': 'admin@gmail.com',
                                'first_name': '', 'last_name': '', 'role': 'employee',
                                'is_staff': True, 'is_active': True,
                            },
                            {
                                'id': 9, 'username': 'localadmin', 'email': 'localadmin@example.com',
                                'first_name': '', 'last_name': '', 'role': 'employee',
                                'is_staff': True, 'is_active': True,
                            },
                            {
                                'id': 10, 'username': 'admin', 'email': 'admin@example.com',
                                'first_name': '', 'last_name': '', 'role': 'employee',
                                'is_staff': True, 'is_active': True,
                            },
                        ]
                        
                        for user_data in users_data:
                            if not User.objects.filter(username=user_data['username']).exists():
                                user = User.objects.create_user(
                                    username=user_data['username'],
                                    email=user_data['email'],
                                    first_name=user_data['first_name'],
                                    last_name=user_data['last_name'],
                                    role=user_data['role'],
                                    is_staff=user_data['is_staff'],
                                    is_active=user_data['is_active'],
                                )
                                user.set_password('defaultpassword123')
                                user.save()
                                print(f"Imported user: {user.username}")
                        
                        # Import votes
                        votes_data = [
                            {'voter_id': 7, 'candidate_id': 1},  # employee1 -> john doe
                            {'voter_id': 1, 'candidate_id': 1},  # Vaahnitha -> john doe
                            {'voter_id': 9, 'candidate_id': 2},  # localadmin -> jane doe
                        ]
                        
                        for vote_data in votes_data:
                            try:
                                voter = User.objects.get(id=vote_data['voter_id'])
                                candidate = Candidate.objects.get(id=vote_data['candidate_id'])
                                
                                if not Vote.objects.filter(voter=voter).exists():
                                    Vote.objects.create(voter=voter, candidate=candidate)
                                    print(f"Imported vote: {voter.username} -> {candidate.name}")
                            except (User.DoesNotExist, Candidate.DoesNotExist):
                                pass
                        
                        print("Local data import completed!")
                else:
                    print(f"Data already exists ({candidate_count} candidates), skipping import")
                    
        except Exception as e:
            # Log import errors but don't block boot
            print(f"Data import error: {e}")
            pass
        
        # Return the application after migrations
        # Fall through to final application assignment below
except Exception:
    # If importing management or calling migrate fails, continue normally
    pass

settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'backend.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()

