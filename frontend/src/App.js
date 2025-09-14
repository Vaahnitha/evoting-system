import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navigation from './components/Navigation';
import Login from './components/Login';
import Voting from './components/Voting';
import Results from './components/Results';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navigation />
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route 
              path="/voting" 
              element={
                <ProtectedRoute>
                  <Voting />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/results" 
              element={
                <ProtectedRoute>
                  <Results />
                </ProtectedRoute>
              } 
            />
            <Route path="/" element={<Navigate to="/voting" replace />} />
            <Route path="*" element={<Navigate to="/voting" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;