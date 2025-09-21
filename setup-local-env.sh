#!/bin/bash

echo "Setting up local environment for E-Voting System..."
echo

echo "Creating .env file for local development..."
cat > .env << 'EOF'
# Local Development Environment Configuration
# This file is for local development only

# Database Configuration - Using SQLite for local development
# Uncomment and configure the line below if you want to use PostgreSQL locally
# DATABASE_URL=postgresql://username:password@localhost:5432/evoting_db

# Admin/Superuser Configuration
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
SEED_ADMIN=true

# Django Configuration
DJANGO_SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=true

# Local Configuration
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF

echo
echo "Installing/updating Python dependencies..."
pip install -r requirements.txt

echo
echo "Running database migrations..."
python backend/manage.py migrate

echo
echo "Setting up admin user..."
python backend/manage.py setup_admin

echo
echo "Local environment setup complete!"
echo
echo "You can now start the development servers with:"
echo "  ./start-dev.sh"
echo
echo "Admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo
