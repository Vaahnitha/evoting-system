# E-Voting MVP System - Knowledge Transfer Document

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Architecture](#3-architecture)
4. [Setup Instructions](#4-setup-instructions)
5. [Environment & Configuration](#5-environment--configuration)
6. [Deployment](#6-deployment)
7. [Usage](#7-usage)
8. [Troubleshooting](#8-troubleshooting)
9. [Future Enhancements](#9-future-enhancements)

---

## 1. Project Overview

### Purpose
The E-Voting MVP System is a secure, web-based voting platform designed for internal organizational elections. It provides a streamlined digital solution for conducting employee elections with real-time results and secure authentication.

### Main Features
- **Secure Authentication**: JWT-based authentication system with role-based access control
- **Vote Casting**: One-time voting mechanism with duplicate prevention
- **Real-time Results**: Live election results with vote counts and percentages (admin-only)
- **Candidate Management**: Add and manage election candidates through Django admin
- **User Management**: Employee and admin user accounts with different privileges
- **Responsive Design**: Mobile-friendly interface built with Bootstrap 5

### Intended Users
- **Employees**: Can login, view candidates, and cast their vote (one-time only)
- **Administrators**: Can access all employee features plus view real-time election results
- **System Administrators**: Full access to Django admin for user and candidate management

---

## 2. Tech Stack

### Backend
- **Framework**: Django 5.2.6 (Python web framework)
- **API**: Django REST Framework 3.15.2
- **Authentication**: JWT tokens via djangorestframework-simplejwt 5.5.1
- **Database**: PostgreSQL (production) / SQLite (development)
- **CORS**: django-cors-headers 4.3.1 for cross-origin requests
- **Server**: Gunicorn 23.0.0 (production WSGI server)
- **Environment**: python-dotenv 1.0.0 for configuration management

### Frontend
- **Framework**: React 19.1.1
- **Routing**: React Router DOM 7.9.1
- **HTTP Client**: Axios 1.12.1
- **UI Framework**: Bootstrap 5.3.0 (via CDN)
- **Build Tool**: Create React App (react-scripts 5.0.1)

### Database
- **Production**: PostgreSQL (managed via Render free tier)
- **Development**: SQLite (file-based database)

### Deployment
- **Backend**: Render (free tier) with PostgreSQL database
- **Frontend**: Vercel (automatic deployment from GitHub)
- **Domain**: Custom domains supported

---

## 3. Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Django Backend │    │   PostgreSQL    │
│   (Vercel)      │◄──►│   (Render)      │◄──►│   Database      │
│                 │    │                 │    │                 │
│ - Authentication│    │ - REST API      │    │ - Users         │
│ - Voting UI     │    │ - JWT Auth      │    │ - Candidates    │
│ - Results       │    │ - Vote Logic    │    │ - Votes         │
│ - Bootstrap UI  │    │ - Admin Panel   │    │ - Audit Trail   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Folder Structure

```
evoting-system/
├── backend/                          # Django backend application
│   ├── backend/                      # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py              # Development settings
│   │   ├── settings_production.py   # Production settings
│   │   ├── urls.py                  # Main URL routing
│   │   ├── wsgi.py                  # WSGI configuration
│   │   └── asgi.py                  # ASGI configuration
│   ├── voting/                      # Main Django app
│   │   ├── models.py                # Database models (User, Candidate, Vote)
│   │   ├── views.py                 # API views and business logic
│   │   ├── serializers.py           # Data serialization
│   │   ├── urls.py                  # API endpoint routing
│   │   ├── admin.py                 # Django admin configuration
│   │   └── management/              # Custom Django commands
│   │       └── commands/
│   │           ├── setup_admin.py   # Admin user creation
│   │           ├── import_local_data.py  # Data import utility
│   │           └── sync_to_production.py # Production sync
│   ├── manage.py                    # Django management script
│   ├── requirements.txt             # Python dependencies
│   └── db.sqlite3                   # SQLite database (development)
├── frontend/                        # React frontend application
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── Login.js             # Authentication component
│   │   │   ├── Voting.js            # Vote casting interface
│   │   │   ├── Results.js           # Results dashboard
│   │   │   ├── Navigation.js        # Navigation component
│   │   │   └── ProtectedRoute.js    # Route protection
│   │   ├── contexts/
│   │   │   └── AuthContext.js       # Authentication context
│   │   ├── services/
│   │   │   └── api.js               # API service layer
│   │   ├── App.js                   # Main React component
│   │   └── index.js                 # React entry point
│   ├── public/                      # Static assets
│   ├── build/                       # Production build output
│   ├── package.json                 # Node.js dependencies
│   └── package-lock.json            # Dependency lock file
├── render.yaml                      # Render deployment configuration
├── vercel.json                      # Vercel deployment configuration
├── requirements.txt                 # Python dependencies (root level)
├── env.example                      # Environment variables template
├── DEPLOYMENT.md                    # Deployment guide
├── SETUP_GUIDE.md                   # Setup instructions
└── README.md                        # Project documentation
```

### Data Flow

1. **Authentication Flow**:
   - User enters credentials → Frontend sends POST to `/api/token/`
   - Backend validates credentials → Returns JWT token
   - Frontend stores token in localStorage → Subsequent requests include Bearer token

2. **Voting Flow**:
   - Authenticated user requests candidates → GET `/api/candidates/`
   - User selects candidate → POST `/api/vote/` with candidate ID
   - Backend validates vote (no duplicates) → Creates Vote record
   - Frontend shows success message → Redirects to results (if admin)

3. **Results Flow**:
   - Admin requests results → GET `/api/results/`
   - Backend aggregates votes → Returns vote counts and percentages
   - Frontend displays results dashboard with charts and tables

---

## 4. Setup Instructions

### Prerequisites
- **Python**: 3.8+ (3.11 recommended for Render compatibility)
- **Node.js**: 14+ (18+ recommended)
- **npm**: Comes with Node.js
- **Git**: For version control
- **PostgreSQL**: For production deployment (optional for local development)

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd evoting-system
   ```

2. **Create and activate virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp ../env.example .env
   # Edit .env file with your configuration
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create admin user**:
   ```bash
   python manage.py setup_admin
   ```

7. **Start development server**:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

### Running Both Locally

The project includes automated startup scripts:

**Windows**:
```bash
# From project root
start-dev.bat
```

**Linux/Mac**:
```bash
# From project root
chmod +x start-dev.sh
./start-dev.sh
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

---

## 5. Environment & Configuration

### Required Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | SQLite for local | Yes for production |
| `DJANGO_SECRET_KEY` | Django secret key | Generated | Yes |
| `DEBUG` | Debug mode | `true` for local | No |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` | Yes for production |
| `CORS_ALLOWED_ORIGINS` | CORS origins | `http://localhost:3000` | Yes for production |
| `ADMIN_USERNAME` | Admin username | `admin` | No |
| `ADMIN_EMAIL` | Admin email | `admin@example.com` | No |
| `ADMIN_PASSWORD` | Admin password | None | Yes |
| `SEED_ADMIN` | Auto-create admin on startup | `false` | No |

### Example .env File

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/evoting_db

# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=false

# Host Configuration
ALLOWED_HOSTS=evoting-system-h779.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://evoting-system-rho.vercel.app,http://localhost:3000

# Admin Configuration
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your_secure_password_here
SEED_ADMIN=true

# Frontend Configuration (for production builds)
REACT_APP_RENDER_BACKEND_URL=https://evoting-system-h779.onrender.com/api
```

### Render Backend Setup

1. **Create new Web Service** on Render
2. **Connect GitHub repository**
3. **Set environment variables** in Render dashboard:
   - `DJANGO_SETTINGS_MODULE=backend.settings_production`
   - `DATABASE_URL` (from PostgreSQL database)
   - `DJANGO_SECRET_KEY` (generate secure key)
   - `ALLOWED_HOSTS` (your Render domain)
   - `CORS_ALLOWED_ORIGINS` (your Vercel frontend URL)
   - `ADMIN_PASSWORD` (secure password)
   - `SEED_ADMIN=true`

### Vercel Frontend Setup

1. **Connect GitHub repository** to Vercel
2. **Set environment variables**:
   - `REACT_APP_RENDER_BACKEND_URL=https://your-backend-name.onrender.com/api`
   - `REACT_APP_FORCE_REMOTE=true`

---

## 6. Deployment

### Backend Deployment (Render)

1. **Database Setup**:
   ```bash
   # Create PostgreSQL database on Render
   # Note the DATABASE_URL connection string
   ```

2. **Service Configuration**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.wsgi:application`
   - **Python Version**: 3.11.0

3. **Environment Variables** (see render.yaml):
   ```bash
   DJANGO_SETTINGS_MODULE=backend.settings_production
   DATABASE_URL=<from-database>
   ALLOWED_HOSTS=your-app-name.onrender.com
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
   DEBUG=false
   ADMIN_PASSWORD=<secure-password>
   SEED_ADMIN=true
   ```

4. **Common Issues**:
   - **ALLOWED_HOSTS**: Must include your Render domain
   - **HTTPS vs HTTP**: Production uses HTTPS, ensure CORS settings match
   - **Database SSL**: PostgreSQL requires SSL in production

### Frontend Deployment (Vercel)

1. **Automatic Deployment**:
   - Connect GitHub repository
   - Vercel auto-detects React app in `frontend/` directory

2. **Build Configuration** (vercel.json):
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "frontend/package.json",
         "use": "@vercel/static-build",
         "config": {
           "distDir": "build"
         }
       }
     ]
   }
   ```

3. **Environment Variables**:
   ```bash
   REACT_APP_RENDER_BACKEND_URL=https://your-backend.onrender.com/api
   REACT_APP_FORCE_REMOTE=true
   ```

4. **Custom Domain**: Configure in Vercel dashboard for production use

---

## 7. Usage

### API Endpoints

#### Authentication
- **POST** `/api/token/` - Login (obtain JWT token)
  ```json
  Request: {"username": "admin", "password": "password123"}
  Response: {"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...", "refresh": "..."}
  ```

- **POST** `/api/token/refresh/` - Refresh JWT token
  ```json
  Request: {"refresh": "refresh_token_here"}
  Response: {"access": "new_access_token"}
  ```

#### Voting Operations
- **GET** `/api/candidates/` - List all candidates (authenticated)
  ```json
  Response: [
    {"id": 1, "name": "John Doe", "department": "Engineering"},
    {"id": 2, "name": "Jane Smith", "department": "HR"}
  ]
  ```

- **POST** `/api/vote/` - Cast a vote (authenticated, one-time only)
  ```json
  Request: {"candidate": 1}
  Response: {"id": 1, "candidate": 1, "timestamp": "2024-01-15T10:30:00Z"}
  ```

#### Results (Admin Only)
- **GET** `/api/results/` - Get election results (admin only)
  ```json
  Response: {
    "total_votes": 25,
    "candidates": [
      {
        "id": 1,
        "name": "John Doe",
        "department": "Engineering",
        "votes": 15,
        "percentage": 60.0
      },
      {
        "id": 2,
        "name": "Jane Smith",
        "department": "HR",
        "votes": 10,
        "percentage": 40.0
      }
    ]
  }
  ```

#### Utility Endpoints
- **GET** `/api/test/` - Test API connectivity (no auth required)
- **POST** `/api/import-data/` - Import sample data (admin only)
- **POST** `/api/reset-admin-password/` - Reset admin password (admin only)

### Frontend Routes

#### React Router Configuration
- **`/login`** - Login page (public)
- **`/voting`** - Vote casting interface (authenticated)
- **`/results`** - Results dashboard (admin only)
- **`/`** - Redirects to `/voting`

#### Component Functionality

**Login Component** (`/login`):
- Username/password authentication
- JWT token storage in localStorage
- Error handling and loading states
- Redirect to voting page on success

**Voting Component** (`/voting`):
- Display candidate cards with Bootstrap styling
- One-click voting with confirmation
- Duplicate vote prevention
- Success message and navigation options
- Logout functionality

**Results Component** (`/results`):
- Admin-only access with permission checking
- Real-time vote counts and percentages
- Visual progress bars and ranking
- Refresh functionality
- Summary statistics cards

### User Workflows

#### Employee Workflow
1. Navigate to application URL
2. Login with provided credentials
3. View available candidates
4. Select and vote for preferred candidate
5. Confirm vote submission
6. Logout or view results (if admin)

#### Admin Workflow
1. Complete employee workflow
2. Access results dashboard
3. View real-time vote counts and percentages
4. Monitor election progress
5. Manage users and candidates via Django admin

---

## 8. Troubleshooting

### Common Local Development Errors

#### 1. CORS Errors
**Symptoms**: Browser shows CORS policy errors, API calls fail
**Solutions**:
```bash
# Check backend is running on port 8000
python manage.py runserver

# Verify CORS settings in backend/backend/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

#### 2. API Connection Failed
**Symptoms**: Frontend shows "API connection failed" or network errors
**Solutions**:
```bash
# Verify backend is running
curl http://localhost:8000/api/test/

# Check API URL in frontend/src/services/api.js
# Should be: http://localhost:8000/api
```

#### 3. Missing Migrations
**Symptoms**: Database errors, missing tables
**Solutions**:
```bash
# Run migrations
python manage.py migrate

# Create superuser if needed
python manage.py setup_admin
```

#### 4. Build Errors
**Symptoms**: Frontend build fails, npm errors
**Solutions**:
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version compatibility
node --version  # Should be 14+
```

### Common Deployment Errors

#### 1. ALLOWED_HOSTS Misconfiguration
**Symptoms**: 400 Bad Request, "Disallowed Host" error
**Solutions**:
```bash
# Update ALLOWED_HOSTS environment variable
ALLOWED_HOSTS=your-app-name.onrender.com

# For multiple domains
ALLOWED_HOSTS=domain1.com,domain2.com,localhost
```

#### 2. Mixed Content HTTP/HTTPS Issue
**Symptoms**: CORS errors in production, mixed content warnings
**Solutions**:
```bash
# Ensure all URLs use HTTPS in production
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
REACT_APP_RENDER_BACKEND_URL=https://your-backend.onrender.com/api
```

#### 3. Database Connection Issues
**Symptoms**: 500 Internal Server Error, database connection failed
**Solutions**:
```bash
# Verify DATABASE_URL format
DATABASE_URL=postgresql://user:password@host:port/database

# Check database SSL requirements
DB_SSL_REQUIRE=true  # Usually required for Render PostgreSQL
```

#### 4. Admin Login Issues
**Symptoms**: Cannot login to Django admin, invalid credentials
**Solutions**:
```bash
# Reset admin password
python manage.py setup_admin --force

# Or create new admin user
python manage.py createsuperuser
```

### Debugging Commands

```bash
# Check environment variables
python -c "import os; print(os.getenv('DATABASE_URL'))"

# Test database connection
python manage.py dbshell

# Check admin users
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print([u.username for u in User.objects.filter(is_superuser=True)])"

# Run migrations manually
python manage.py migrate

# Import sample data
python manage.py import_local_data

# Test API endpoints
curl -X GET http://localhost:8000/api/test/
curl -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"admin","password":"password"}'
```

### Log Analysis

#### Render Logs
- Access Render dashboard → Service → Logs
- Look for Django errors, database connection issues
- Check environment variable loading

#### Vercel Logs
- Access Vercel dashboard → Project → Functions → Logs
- Look for build errors, runtime errors
- Check environment variable configuration

---

## 9. Future Enhancements

### Planned Features

#### 1. Enhanced Admin Panel
- **Real-time Dashboard**: Live election monitoring with WebSocket updates
- **Advanced Analytics**: Vote distribution charts, participation metrics
- **Audit Logging**: Complete vote trail with timestamps and user tracking
- **Bulk User Management**: CSV import/export for user accounts

#### 2. Security Improvements
- **Two-Factor Authentication**: SMS or email-based 2FA for admin accounts
- **Vote Encryption**: End-to-end encryption for vote data
- **Rate Limiting**: API rate limiting to prevent abuse
- **Session Management**: Advanced session handling with device tracking

#### 3. User Experience Enhancements
- **Mobile App**: React Native mobile application
- **Offline Voting**: Offline capability with sync when online
- **Multi-language Support**: Internationalization (i18n)
- **Accessibility**: WCAG 2.1 compliance for screen readers

#### 4. Advanced Voting Features
- **Multiple Elections**: Support for concurrent elections
- **Ranked Choice Voting**: Alternative voting systems
- **Vote Delegation**: Proxy voting capabilities
- **Election Scheduling**: Automated election start/end times

### Scaling Considerations

#### 1. Database Optimization
- **Connection Pooling**: Implement database connection pooling
- **Read Replicas**: Separate read/write database instances
- **Caching**: Redis for session storage and API caching
- **Database Sharding**: Horizontal scaling for large user bases

#### 2. Infrastructure Scaling
- **Load Balancing**: Multiple backend instances behind load balancer
- **CDN Integration**: Static asset delivery via CDN
- **Auto-scaling**: Dynamic scaling based on traffic
- **Microservices**: Split into smaller, focused services

#### 3. Performance Optimization
- **API Optimization**: GraphQL for efficient data fetching
- **Frontend Optimization**: Code splitting, lazy loading
- **Database Indexing**: Optimize query performance
- **Caching Strategy**: Multi-level caching implementation

### Production Readiness Checklist

#### Security
- [ ] Implement HTTPS everywhere
- [ ] Set up proper firewall rules
- [ ] Regular security audits
- [ ] Backup and disaster recovery plan
- [ ] GDPR compliance for user data

#### Monitoring
- [ ] Application performance monitoring (APM)
- [ ] Error tracking and alerting
- [ ] Uptime monitoring
- [ ] Database performance monitoring
- [ ] User analytics and behavior tracking

#### Maintenance
- [ ] Automated testing pipeline
- [ ] Continuous integration/deployment
- [ ] Regular dependency updates
- [ ] Database backup automation
- [ ] Documentation maintenance

---

## Conclusion

This E-Voting MVP System provides a solid foundation for digital elections with room for significant expansion. The modular architecture, comprehensive documentation, and deployment-ready configuration make it suitable for both immediate use and long-term development.

For questions or support, refer to the troubleshooting section or consult the existing documentation files in the repository.

---

**Document Version**: 1.0  
**Last Updated**: January 2024  
**Maintained By**: Development Team
