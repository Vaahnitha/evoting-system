import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from voting.models import Candidate, Vote
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Import local data to production database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing data before import',
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting data import...')
        
        # Check if we're in production
        if not self.is_production_database():
            self.stdout.write(
                self.style.WARNING('This command should be run in production environment!')
            )
            response = input('Continue anyway? (y/N): ')
            if response.lower() != 'y':
                self.stdout.write('Import cancelled.')
                return
        
        # Clear existing data if requested
        if options['clear_existing']:
            self.stdout.write('Clearing existing data...')
            with transaction.atomic():
                Vote.objects.all().delete()
                Candidate.objects.all().delete()
                User.objects.filter(is_superuser=False).delete()  # Keep superusers
            self.stdout.write('Existing data cleared!')
        
        # Import candidates
        candidates_imported = self.import_candidates()
        
        # Import users
        users_imported = self.import_users()
        
        # Import votes
        votes_imported = self.import_votes()
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write('IMPORT SUMMARY')
        self.stdout.write('='*50)
        self.stdout.write(f'Candidates imported: {candidates_imported}')
        self.stdout.write(f'Users imported: {users_imported}')
        self.stdout.write(f'Votes imported: {votes_imported}')
        self.stdout.write('='*50)
        
        self.stdout.write(
            self.style.SUCCESS('Data import completed successfully!')
        )

    def import_candidates(self):
        """Import candidates from JSON data"""
        candidates_data = self.get_candidates_data()
        imported_count = 0
        
        self.stdout.write('Importing candidates...')
        
        for candidate_data in candidates_data:
            candidate, created = Candidate.objects.get_or_create(
                id=candidate_data['id'],
                defaults={
                    'name': candidate_data['name'],
                    'department': candidate_data['department'],
                }
            )
            if created:
                imported_count += 1
                self.stdout.write(f'  Created candidate: {candidate.name}')
            else:
                self.stdout.write(f'  Candidate already exists: {candidate.name}')
        
        self.stdout.write(f'Imported {imported_count} candidates')
        return imported_count

    def import_users(self):
        """Import users from JSON data"""
        users_data = self.get_users_data()
        imported_count = 0
        
        self.stdout.write('Importing users...')
        
        for user_data in users_data:
            # Skip if user already exists
            if User.objects.filter(username=user_data['username']).exists():
                self.stdout.write(f'  User already exists: {user_data["username"]}')
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
            
            # Set a default password (users will need to reset)
            user.set_password('defaultpassword123')
            user.save()
            
            imported_count += 1
            self.stdout.write(f'  Created user: {user.username}')
        
        self.stdout.write(f'Imported {imported_count} users')
        return imported_count

    def import_votes(self):
        """Import votes from JSON data"""
        votes_data = self.get_votes_data()
        imported_count = 0
        
        self.stdout.write('Importing votes...')
        
        for vote_data in votes_data:
            try:
                voter = User.objects.get(id=vote_data['voter_id'])
                candidate = Candidate.objects.get(id=vote_data['candidate_id'])
                
                # Skip if vote already exists for this voter
                if Vote.objects.filter(voter=voter).exists():
                    self.stdout.write(f'  Vote already exists for user: {voter.username}')
                    continue
                
                Vote.objects.create(
                    voter=voter,
                    candidate=candidate,
                )
                imported_count += 1
                self.stdout.write(f'  Created vote: {voter.username} -> {candidate.name}')
                
            except User.DoesNotExist:
                self.stdout.write(f'  Voter with id {vote_data["voter_id"]} not found, skipping vote...')
            except Candidate.DoesNotExist:
                self.stdout.write(f'  Candidate with id {vote_data["candidate_id"]} not found, skipping vote...')
            except Exception as e:
                self.stdout.write(f'  Error importing vote: {e}')
        
        self.stdout.write(f'Imported {imported_count} votes')
        return imported_count

    def get_candidates_data(self):
        """Get candidates data - either from JSON file or hardcoded"""
        # Try to load from JSON file first
        if os.path.exists('candidates_export.json'):
            with open('candidates_export.json', 'r') as f:
                return json.load(f)
        
        # Fallback to hardcoded data
        return [
            {'id': 1, 'name': 'john doe', 'department': 'eng'},
            {'id': 2, 'name': 'jane doe', 'department': 'hr'},
            {'id': 3, 'name': 'alex b', 'department': 'pm'},
            {'id': 4, 'name': 'cow', 'department': 'moo'},
        ]

    def get_users_data(self):
        """Get users data - either from JSON file or hardcoded"""
        # Try to load from JSON file first
        if os.path.exists('users_export.json'):
            with open('users_export.json', 'r') as f:
                return json.load(f)
        
        # Fallback to hardcoded data
        return [
            {
                'id': 1, 'username': 'Vaahnitha', 'email': 'vaahnithachowdary.ch@gmail.com',
                'first_name': '', 'last_name': '', 'role': 'employee',
                'is_staff': True, 'is_active': True,
                'date_joined': '2025-09-12 15:58:52.357142', 'last_login': '2025-09-15 15:40:42.839580'
            },
            {
                'id': 7, 'username': 'employee1', 'email': '',
                'first_name': '', 'last_name': '', 'role': 'employee',
                'is_staff': False, 'is_active': True,
                'date_joined': '2025-09-14 08:18:52.654540', 'last_login': None
            },
            {
                'id': 8, 'username': 'Admin', 'email': 'admin@gmail.com',
                'first_name': '', 'last_name': '', 'role': 'employee',
                'is_staff': True, 'is_active': True,
                'date_joined': '2025-09-15 16:47:04.111568', 'last_login': None
            },
            {
                'id': 9, 'username': 'localadmin', 'email': 'localadmin@example.com',
                'first_name': '', 'last_name': '', 'role': 'employee',
                'is_staff': True, 'is_active': True,
                'date_joined': '2025-09-15 16:54:26.448132', 'last_login': None
            },
            {
                'id': 10, 'username': 'admin', 'email': 'admin@example.com',
                'first_name': '', 'last_name': '', 'role': 'employee',
                'is_staff': True, 'is_active': True,
                'date_joined': '2025-09-17 04:57:22.834552', 'last_login': None
            },
        ]

    def get_votes_data(self):
        """Get votes data - either from JSON file or hardcoded"""
        # Try to load from JSON file first
        if os.path.exists('votes_export.json'):
            with open('votes_export.json', 'r') as f:
                return json.load(f)
        
        # Fallback to hardcoded data
        return [
            {'id': 2, 'voter_id': 7, 'candidate_id': 1, 'timestamp': '2025-09-14 08:21:46.871167'},
            {'id': 3, 'voter_id': 1, 'candidate_id': 1, 'timestamp': '2025-09-14 09:38:13.076300'},
            {'id': 4, 'voter_id': 9, 'candidate_id': 2, 'timestamp': '2025-09-15 17:23:40.592699'},
        ]

    def is_production_database(self):
        """Check if we're connected to production database"""
        from django.conf import settings
        db_config = settings.DATABASES['default']
        return db_config['ENGINE'] == 'django.db.backends.postgresql'
