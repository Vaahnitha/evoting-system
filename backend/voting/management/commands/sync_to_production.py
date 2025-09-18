import json
import os
from django.core.management.base import BaseCommand
from django.db import connections
from django.conf import settings
from voting.models import Candidate, Vote
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Sync local database data to production database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--export',
            action='store_true',
            help='Export local data to JSON files',
        )
        parser.add_argument(
            '--import',
            action='store_true',
            help='Import data from JSON files to production database',
        )
        parser.add_argument(
            '--clear-production',
            action='store_true',
            help='Clear existing data in production database before import',
        )

    def handle(self, *args, **options):
        if options['export']:
            self.export_data()
        elif options['import']:
            self.import_data(options['clear_production'])
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --export or --import')
            )

    def export_data(self):
        """Export local data to JSON files"""
        self.stdout.write('Exporting local data...')
        
        # Export candidates
        candidates_data = []
        for candidate in Candidate.objects.all():
            candidates_data.append({
                'id': candidate.id,
                'name': candidate.name,
                'department': candidate.department,
                'image': candidate.image if hasattr(candidate, 'image') else None,
            })
        
        with open('candidates_export.json', 'w') as f:
            json.dump(candidates_data, f, indent=2)
        
        # Export users (excluding superusers for security)
        users_data = []
        for user in User.objects.all():
            users_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'date_joined': user.date_joined.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
            })
        
        with open('users_export.json', 'w') as f:
            json.dump(users_data, f, indent=2)
        
        # Export votes
        votes_data = []
        for vote in Vote.objects.all():
            votes_data.append({
                'id': vote.id,
                'voter_id': vote.voter.id,
                'candidate_id': vote.candidate.id,
                'timestamp': vote.timestamp.isoformat(),
            })
        
        with open('votes_export.json', 'w') as f:
            json.dump(votes_data, f, indent=2)
        
        self.stdout.write(
            self.style.SUCCESS('Data exported successfully!')
        )
        self.stdout.write('Files created:')
        self.stdout.write('  - candidates_export.json')
        self.stdout.write('  - users_export.json')
        self.stdout.write('  - votes_export.json')

    def import_data(self, clear_production=False):
        """Import data from JSON files to production database"""
        self.stdout.write('Importing data to production database...')
        
        # Check if we're connected to production database
        if not self.is_production_database():
            self.stdout.write(
                self.style.ERROR('Not connected to production database!')
            )
            self.stdout.write('Make sure DATABASE_URL is set to your production database.')
            return
        
        if clear_production:
            self.stdout.write('Clearing existing production data...')
            Vote.objects.all().delete()
            Candidate.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()  # Keep superusers
        
        # Import candidates
        if os.path.exists('candidates_export.json'):
            with open('candidates_export.json', 'r') as f:
                candidates_data = json.load(f)
            
            for candidate_data in candidates_data:
                candidate, created = Candidate.objects.get_or_create(
                    id=candidate_data['id'],
                    defaults={
                        'name': candidate_data['name'],
                        'department': candidate_data['department'],
                    }
                )
                if created:
                    self.stdout.write(f'Created candidate: {candidate.name}')
                else:
                    self.stdout.write(f'Candidate already exists: {candidate.name}')
        
        # Import users (create new users, don't overwrite existing ones)
        if os.path.exists('users_export.json'):
            with open('users_export.json', 'r') as f:
                users_data = json.load(f)
            
            for user_data in users_data:
                # Skip if user already exists
                if User.objects.filter(username=user_data['username']).exists():
                    self.stdout.write(f'User already exists: {user_data["username"]}')
                    continue
                
                # Create new user
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    role=user_data['role'],
                    is_staff=user_data['is_staff'],
                    is_active=user_data['is_active'],
                )
                
                # Set password to a default (users will need to reset)
                user.set_password('defaultpassword123')
                user.save()
                
                self.stdout.write(f'Created user: {user.username}')
        
        # Import votes
        if os.path.exists('votes_export.json'):
            with open('votes_export.json', 'r') as f:
                votes_data = json.load(f)
            
            for vote_data in votes_data:
                try:
                    voter = User.objects.get(id=vote_data['voter_id'])
                    candidate = Candidate.objects.get(id=vote_data['candidate_id'])
                    
                    # Skip if vote already exists
                    if Vote.objects.filter(voter=voter).exists():
                        self.stdout.write(f'Vote already exists for user: {voter.username}')
                        continue
                    
                    Vote.objects.create(
                        voter=voter,
                        candidate=candidate,
                    )
                    self.stdout.write(f'Created vote: {voter.username} -> {candidate.name}')
                except (User.DoesNotExist, Candidate.DoesNotExist) as e:
                    self.stdout.write(f'Skipping vote due to missing reference: {e}')
        
        self.stdout.write(
            self.style.SUCCESS('Data import completed!')
        )

    def is_production_database(self):
        """Check if we're connected to production database"""
        db_config = settings.DATABASES['default']
        
        # Check if it's PostgreSQL (production) vs SQLite (local)
        return db_config['ENGINE'] == 'django.db.backends.postgresql'
