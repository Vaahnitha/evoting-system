import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { resultsAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Results = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login');
      return;
    }
    fetchResults();
  }, [isAuthenticated, navigate]);

  const fetchResults = async () => {
    try {
      const response = await resultsAPI.getResults();
      setResults(response.data);
    } catch (error) {
      if (error.response?.status === 403) {
        setError('Access denied. Admin privileges required to view results.');
      } else {
        setError('Error loading results. Please try again.');
      }
      console.error('Error fetching results:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleRefresh = () => {
    setLoading(true);
    setError('');
    fetchResults();
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="row justify-content-center">
          <div className="col-md-6 text-center">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3">Loading results...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="alert alert-danger text-center">
              <i className="bi bi-exclamation-triangle me-2"></i>
              {error}
            </div>
            <div className="text-center">
              <button className="btn btn-primary me-2" onClick={handleRefresh}>
                <i className="bi bi-arrow-clockwise me-2"></i>
                Try Again
              </button>
              <button className="btn btn-outline-secondary" onClick={handleLogout}>
                <i className="bi bi-box-arrow-right me-2"></i>
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const { total_votes, candidates } = results;
  const maxVotes = Math.max(...candidates.map(c => c.votes));

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h1 className="h2">
              <i className="bi bi-bar-chart text-primary me-2"></i>
              Election Results
            </h1>
            <div>
              <button 
                className="btn btn-outline-primary me-2"
                onClick={handleRefresh}
              >
                <i className="bi bi-arrow-clockwise me-2"></i>
                Refresh
              </button>
              <button 
                className="btn btn-outline-danger"
                onClick={handleLogout}
              >
                <i className="bi bi-box-arrow-right me-2"></i>
                Logout
              </button>
            </div>
          </div>

          {/* Summary Card */}
          <div className="row mb-4">
            <div className="col-md-4">
              <div className="card bg-primary text-white">
                <div className="card-body text-center">
                  <i className="bi bi-people" style={{ fontSize: '2rem' }}></i>
                  <h3 className="mt-2">{total_votes}</h3>
                  <p className="mb-0">Total Votes</p>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card bg-success text-white">
                <div className="card-body text-center">
                  <i className="bi bi-person-check" style={{ fontSize: '2rem' }}></i>
                  <h3 className="mt-2">{candidates.length}</h3>
                  <p className="mb-0">Candidates</p>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="card bg-info text-white">
                <div className="card-body text-center">
                  <i className="bi bi-trophy" style={{ fontSize: '2rem' }}></i>
                  <h3 className="mt-2">
                    {candidates.find(c => c.votes === maxVotes)?.name || 'N/A'}
                  </h3>
                  <p className="mb-0">Leading</p>
                </div>
              </div>
            </div>
          </div>

          {/* Results Table */}
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">
                <i className="bi bi-list-ol me-2"></i>
                Detailed Results
              </h5>
            </div>
            <div className="card-body">
              {candidates.length === 0 ? (
                <div className="text-center py-4">
                  <i className="bi bi-info-circle text-muted" style={{ fontSize: '3rem' }}></i>
                  <p className="text-muted mt-3">No candidates or votes found.</p>
                </div>
              ) : (
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead className="table-light">
                      <tr>
                        <th>Rank</th>
                        <th>Candidate</th>
                        <th>Department</th>
                        <th>Votes</th>
                        <th>Percentage</th>
                        <th>Progress</th>
                      </tr>
                    </thead>
                    <tbody>
                      {candidates
                        .sort((a, b) => b.votes - a.votes)
                        .map((candidate, index) => (
                          <tr key={candidate.id} className={candidate.votes === maxVotes ? 'table-success' : ''}>
                            <td>
                              <span className={`badge ${index === 0 ? 'bg-warning' : index === 1 ? 'bg-secondary' : index === 2 ? 'bg-warning' : 'bg-light text-dark'}`}>
                                {index + 1}
                              </span>
                            </td>
                            <td>
                              <div className="d-flex align-items-center">
                                <div 
                                  className="rounded-circle me-3 d-flex align-items-center justify-content-center bg-light"
                                  style={{ width: '40px', height: '40px' }}
                                >
                                  <i className="bi bi-person text-muted"></i>
                                </div>
                                <div>
                                  <strong>{candidate.name}</strong>
                                  {candidate.votes === maxVotes && (
                                    <i className="bi bi-trophy-fill text-warning ms-2"></i>
                                  )}
                                </div>
                              </div>
                            </td>
                            <td>{candidate.department || 'N/A'}</td>
                            <td>
                              <span className="badge bg-primary">{candidate.votes}</span>
                            </td>
                            <td>
                              <strong>{candidate.percentage}%</strong>
                            </td>
                            <td>
                              <div className="progress" style={{ height: '20px' }}>
                                <div 
                                  className="progress-bar" 
                                  role="progressbar" 
                                  style={{ width: `${candidate.percentage}%` }}
                                  aria-valuenow={candidate.percentage}
                                  aria-valuemin="0" 
                                  aria-valuemax="100"
                                >
                                  {candidate.percentage}%
                                </div>
                              </div>
                            </td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>

          {/* Last Updated */}
          <div className="text-center mt-4">
            <small className="text-muted">
              <i className="bi bi-clock me-1"></i>
              Last updated: {new Date().toLocaleString()}
            </small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
