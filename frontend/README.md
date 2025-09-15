Environment configuration
-------------------------

For production builds (e.g. on Vercel/Netlify or any static host), set:

```
REACT_APP_RENDER_BACKEND_URL=https://evoting-system-h779.onrender.com/api
```

For local development no env is required; the app defaults to `http://localhost:8000/api`.

# E-Voting System Frontend

A React-based frontend application for the E-Voting System that connects to a Django REST API backend.

## Features

- **Authentication**: JWT-based login system
- **Voting Interface**: Clean, user-friendly voting page with candidate cards
- **Results Dashboard**: Real-time election results with charts and statistics
- **Responsive Design**: Bootstrap-powered responsive UI
- **Error Handling**: Comprehensive error handling and user feedback
- **Security**: Protected routes and automatic token management

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Django backend running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will open in your browser at `http://localhost:3000`.

## API Configuration

The frontend is configured to connect to the Django backend at `http://localhost:8000/api`. If your backend runs on a different port or domain, update the `baseURL` in `src/services/api.js`.

## Project Structure

```
src/
├── components/          # React components
│   ├── Login.js        # Login page component
│   ├── Voting.js       # Voting interface component
│   ├── Results.js      # Results dashboard component
│   ├── Navigation.js   # Navigation bar component
│   └── ProtectedRoute.js # Route protection component
├── contexts/           # React contexts
│   └── AuthContext.js  # Authentication context
├── services/           # API services
│   └── api.js         # Axios configuration and API calls
├── App.js             # Main application component
├── App.css            # Custom styles
├── index.js           # Application entry point
└── index.css          # Base styles
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (one-way operation)

## Features Overview

### Login Page
- Username and password authentication
- JWT token storage in localStorage
- Error handling for invalid credentials
- Responsive design with Bootstrap

### Voting Page
- Displays all candidates in card format
- One-click voting with confirmation
- Prevents duplicate voting
- Success/error message display
- Automatic redirect after voting

### Results Page
- Real-time election results
- Total votes and candidate statistics
- Percentage calculations and progress bars
- Admin-only access (handled by backend)
- Responsive table layout

### Navigation
- Clean navigation bar with Bootstrap
- Active route highlighting
- Logout functionality
- Responsive mobile menu

## API Endpoints

The frontend communicates with these Django REST API endpoints:

- `POST /api/token/` - User authentication
- `GET /api/candidates/` - Fetch candidate list
- `POST /api/vote/` - Cast a vote
- `GET /api/results/` - Fetch election results

## Security Features

- JWT token authentication
- Automatic token inclusion in API requests
- Token expiration handling
- Protected routes for authenticated users
- Secure logout with token cleanup

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your Django backend has CORS configured for `http://localhost:3000`
2. **API Connection**: Verify the backend is running on `http://localhost:8000`
3. **Token Issues**: Clear localStorage and try logging in again
4. **Build Errors**: Delete `node_modules` and run `npm install` again

### Development Tips

- Use browser developer tools to monitor API requests
- Check the Network tab for failed requests
- Verify JWT token in localStorage after login
- Test with different user roles (employee vs admin)

## Contributing

1. Follow the existing code style
2. Add comments for complex logic
3. Test all functionality before submitting
4. Update documentation as needed

## License

This project is part of the E-Voting System and follows the same license terms.