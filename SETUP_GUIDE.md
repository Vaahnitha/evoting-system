# E-Voting System Setup Guide

This guide will help you set up the E-Voting System for both local development and production deployment on Render.

## 🚀 Quick Start (Local Development)

### Option 1: Automated Setup (Recommended)
```bash
# Windows
setup-local-env.bat

# Linux/Mac
chmod +x setup-local-env.sh
./setup-local-env.sh
```

### Option 2: Manual Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   ```bash
   # Copy the example and edit as needed
   cp env.example .env
   
   # Generate a secure secret key for production
   python generate-secret-key.py
   ```

3. **Run migrations:**
   ```bash
   python backend/manage.py migrate
   ```

4. **Create admin user:**
   ```bash
   python backend/manage.py setup_admin
   ```

5. **Start development servers:**
   ```bash
   # Windows
   start-dev.bat
   
   # Linux/Mac
   ./start-dev.sh
   ```

## 🌐 Production Deployment on Render

### Step 1: Create PostgreSQL Database on Render
1. Go to your Render dashboard
2. Create a new PostgreSQL database
3. Note the connection string (DATABASE_URL)

### Step 2: Deploy Backend
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the following configuration:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn backend.wsgi:application
```

**Environment Variables:**
```
DJANGO_SETTINGS_MODULE=backend.settings_production
DJANGO_SECRET_KEY=your-secure-secret-key-here
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your_secure_password_here
SEED_ADMIN=true
ALLOWED_HOSTS=your-app-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
DEBUG=false
DATABASE_URL=postgresql://username:password@hostname:port/database
```

**Important:** Generate a secure `DJANGO_SECRET_KEY` using:
```bash
python generate-secret-key.py
```

### Step 3: Deploy Frontend
1. Create a new Static Site on Render
2. Connect your repository
3. Set the following environment variable:
```
REACT_APP_RENDER_BACKEND_URL=https://your-backend-name.onrender.com/api
```

## 🔧 Configuration Details

### Database Configuration

**Local Development:**
- Default: SQLite (no setup required)
- Optional: PostgreSQL (set `DATABASE_URL` in `.env`)

**Production:**
- Required: PostgreSQL (set `DATABASE_URL` in Render environment variables)

### Admin Credentials

**Default Credentials:**
- Username: `admin`
- Email: `admin@example.com`
- Password: Set via `ADMIN_PASSWORD` environment variable

**To change credentials:**
1. Update environment variables
2. Run: `python backend/manage.py setup_admin --force`

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | SQLite for local | Yes for production |
| `ADMIN_USERNAME` | Admin username | `admin` | No |
| `ADMIN_EMAIL` | Admin email | `admin@example.com` | No |
| `ADMIN_PASSWORD` | Admin password | None | Yes |
| `SEED_ADMIN` | Auto-create admin on startup | `false` | No |
| `DJANGO_SECRET_KEY` | Django secret key | Generated | Yes |
| `DEBUG` | Debug mode | `true` for local | No |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` | Yes for production |
| `CORS_ALLOWED_ORIGINS` | CORS origins | `http://localhost:3000` | Yes for production |

## 🐛 Troubleshooting

### Common Issues

1. **Internal Server Error on Render:**
   - Check that all required environment variables are set
   - Verify `DATABASE_URL` is correct
   - Check Render logs for specific error messages

2. **Database Connection Issues:**
   - Verify `DATABASE_URL` format
   - Ensure database is accessible from Render
   - Check SSL requirements

3. **Admin Login Issues:**
   - Run `python backend/manage.py setup_admin --force`
   - Verify `ADMIN_PASSWORD` is set correctly

4. **CORS Errors:**
   - Update `CORS_ALLOWED_ORIGINS` with your frontend URL
   - Ensure frontend URL matches exactly

### Debugging Commands

```bash
# Check environment variables
python -c "import os; print(os.getenv('DATABASE_URL'))"

# Test database connection
python backend/manage.py dbshell

# Check admin users
python backend/manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print([u.username for u in User.objects.filter(is_superuser=True)])"

# Run migrations manually
python backend/manage.py migrate

# Create admin manually
python backend/manage.py setup_admin
```

## 📱 Access Points

### Local Development
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Django Admin: http://localhost:8000/admin

### Production
- Frontend: https://your-frontend-domain.com
- Backend API: https://your-backend-name.onrender.com/api
- Django Admin: https://your-backend-name.onrender.com/admin

## 🔐 Security Notes

### Environment Variables Security
1. **Never commit `.env` files** to version control - they're automatically ignored
2. **Use the `generate-secret-key.py` script** to create secure secret keys
3. **Use different secret keys** for different environments (dev/staging/production)
4. **Keep all sensitive data** in environment variables, never in code

### Production Security
1. **Use strong passwords** for production (at least 12 characters)
2. **Keep `DEBUG=False`** in production
3. **Use HTTPS** for production deployments
4. **Regularly update dependencies**
5. **Monitor logs** for suspicious activity
6. **Use secure database connections** (SSL enabled)

### Development Security
1. **Use development-specific keys** (not production keys)
2. **Keep DEBUG=True** only for local development
3. **Use strong admin passwords** even in development
4. **Don't share `.env` files** between team members

## 📞 Support

If you encounter issues:
1. Check the logs in Render dashboard
2. Verify all environment variables are set
3. Test locally first to isolate issues
4. Check this guide for common solutions
