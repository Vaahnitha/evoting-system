import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navigation = () => {
  const { isAuthenticated, logout } = useAuth();
  const location = useLocation();

  const handleLogout = () => {
    logout();
  };

  if (!isAuthenticated()) {
    return null;
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link className="navbar-brand" to="/voting">
          <i className="bi bi-shield-check me-2"></i>
          E-Voting System
        </Link>
        
        <button 
          className="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link 
                className={`nav-link ${location.pathname === '/voting' ? 'active' : ''}`} 
                to="/voting"
              >
                <i className="bi bi-ballot-check me-1"></i>
                Voting
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                className={`nav-link ${location.pathname === '/results' ? 'active' : ''}`} 
                to="/results"
              >
                <i className="bi bi-bar-chart me-1"></i>
                Results
              </Link>
            </li>
          </ul>
          
          <ul className="navbar-nav">
            <li className="nav-item">
              <button 
                className="btn btn-outline-light"
                onClick={handleLogout}
              >
                <i className="bi bi-box-arrow-right me-1"></i>
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
