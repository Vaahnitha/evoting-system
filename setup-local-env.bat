@echo off
echo Setting up local environment for E-Voting System...
echo.

echo Creating .env file for local development...
(
echo # Local Development Environment Configuration
echo # This file is for local development only
echo.
echo # Database Configuration - Using SQLite for local development
echo # Uncomment and configure the line below if you want to use PostgreSQL locally
echo # DATABASE_URL=postgresql://username:password@localhost:5432/evoting_db
echo.
echo # Admin/Superuser Configuration
echo ADMIN_USERNAME=admin
echo ADMIN_EMAIL=admin@example.com
echo ADMIN_PASSWORD=admin123
echo SEED_ADMIN=true
echo.
echo # Django Configuration
echo DJANGO_SECRET_KEY=django-insecure-dev-key-change-in-production
echo DEBUG=true
echo.
echo # Local Configuration
echo ALLOWED_HOSTS=localhost,127.0.0.1
echo CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
) > .env

echo.
echo Installing/updating Python dependencies...
venv\Scripts\pip.exe install -r requirements.txt

echo.
echo Running database migrations...
venv\Scripts\python.exe backend\manage.py migrate

echo.
echo Setting up admin user...
venv\Scripts\python.exe backend\manage.py setup_admin

echo.
echo Local environment setup complete!
echo.
echo You can now start the development servers with:
echo   start-dev.bat
echo.
echo Admin credentials:
echo   Username: admin
echo   Password: admin123
echo.
pause
