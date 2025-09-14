@echo off
echo Starting E-Voting System Development Environment...
echo.

echo Starting Django Backend...
start "Django Backend" cmd /k "cd backend && python manage.py runserver"

echo.
echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak > nul

echo Starting React Frontend...
start "React Frontend" cmd /k "cd frontend && npm start"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
