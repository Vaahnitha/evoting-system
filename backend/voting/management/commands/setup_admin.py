"""
Management command to create or update admin superuser.
This ensures consistent admin setup across environments.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create or update admin superuser with environment variables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing admin user password',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get admin credentials from environment variables
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD')
        
        if not admin_password:
            self.stdout.write(
                self.style.ERROR(
                    'ADMIN_PASSWORD environment variable is required. '
                    'Please set it in your .env file or environment.'
                )
            )
            return
        
        # Check if admin user already exists
        try:
            admin_user = User.objects.get(username=admin_username)
            
            if options['force']:
                # Update existing user
                admin_user.email = admin_email
                admin_user.set_password(admin_password)
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully updated admin user: {admin_username}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Admin user {admin_username} already exists. '
                        'Use --force to update password.'
                    )
                )
        except User.DoesNotExist:
            # Create new admin user
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created admin user: {admin_username}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Admin credentials:\n'
                f'  Username: {admin_username}\n'
                f'  Email: {admin_email}\n'
                f'  Password: [set via ADMIN_PASSWORD env var]'
            )
        )
