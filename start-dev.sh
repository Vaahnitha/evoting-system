#!/bin/bash

echo "Starting E-Voting System Development Environment..."
echo

echo "Starting Django Backend..."
cd backend
python manage.py runserver &
BACKEND_PID=$!

echo
echo "Waiting 3 seconds for backend to start..."
sleep 3

echo "Starting React Frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo
echo "Both servers are starting..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop both servers"

# Function to cleanup processes on exit
cleanup() {
    echo
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Trap Ctrl+C
trap cleanup INT

# Wait for user to stop
wait
