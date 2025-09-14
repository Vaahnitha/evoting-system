import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { candidatesAPI, voteAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Voting = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [voting, setVoting] = useState(false);
  const [message, setMessage] = useState('');
  const [hasVoted, setHasVoted] = useState(false);
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/login');
      return;
    }
    fetchCandidates();
  }, [isAuthenticated, navigate]);

  const fetchCandidates = async () => {
    try {
      const response = await candidatesAPI.getCandidates();
      setCandidates(response.data);
    } catch (error) {
      console.error('Error fetching candidates:', error);
      setMessage('Error loading candidates. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleVote = async (candidateId) => {
    setVoting(true);
    setMessage('');

    try {
      await voteAPI.castVote(candidateId);
      setMessage('Vote cast successfully! Thank you for participating.');
      setHasVoted(true);
    } catch (error) {
      if (error.response?.data?.non_field_errors?.[0] === 'You have already voted.') {
        setMessage('You have already voted.');
        setHasVoted(true);
      } else {
        setMessage(
          error.response?.data?.detail || 
          'Error casting vote. Please try again.'
        );
      }
    } finally {
      setVoting(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="row justify-content-center">
          <div className="col-md-6 text-center">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3">Loading candidates...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-12">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h1 className="h2">
              <i className="bi bi-ballot-check text-primary me-2"></i>
              Cast Your Vote
            </h1>
            <button 
              className="btn btn-outline-danger"
              onClick={handleLogout}
            >
              <i className="bi bi-box-arrow-right me-2"></i>
              Logout
            </button>
          </div>

          {message && (
            <div className={`alert ${hasVoted ? 'alert-success' : 'alert-warning'} alert-dismissible fade show`} role="alert">
              <i className={`bi ${hasVoted ? 'bi-check-circle' : 'bi-exclamation-triangle'} me-2`}></i>
              {message}
              <button 
                type="button" 
                className="btn-close" 
                onClick={() => setMessage('')}
              ></button>
            </div>
          )}

          {hasVoted ? (
            <div className="row justify-content-center">
              <div className="col-md-8">
                <div className="card border-success">
                  <div className="card-body text-center py-5">
                    <i className="bi bi-check-circle-fill text-success" style={{ fontSize: '4rem' }}></i>
                    <h3 className="mt-3 text-success">Vote Submitted Successfully!</h3>
                    <p className="text-muted mt-3">
                      Thank you for participating in the election. Your vote has been recorded.
                    </p>
                    <div className="mt-4">
                      <button 
                        className="btn btn-primary me-2"
                        onClick={() => navigate('/results')}
                      >
                        <i className="bi bi-bar-chart me-2"></i>
                        View Results
                      </button>
                      <button 
                        className="btn btn-outline-secondary"
                        onClick={handleLogout}
                      >
                        <i className="bi bi-box-arrow-right me-2"></i>
                        Logout
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="row">
              {candidates.length === 0 ? (
                <div className="col-12">
                  <div className="alert alert-info text-center">
                    <i className="bi bi-info-circle me-2"></i>
                    No candidates available at the moment.
                  </div>
                </div>
              ) : (
                candidates.map((candidate) => (
                  <div key={candidate.id} className="col-md-6 col-lg-4 mb-4">
                    <div className="card h-100 shadow-sm">
                      <div className="card-body d-flex flex-column">
                        <div className="text-center mb-3">
                          <i 
                            className="bi bi-person-circle text-primary" 
                            style={{ 
                              fontSize: '3rem',
                            }}
                          ></i>
                        </div>
                        <h5 className="card-title text-center">{candidate.name}</h5>
                        <p className="card-text text-center text-muted">
                          <i className="bi bi-building me-1"></i>
                          {candidate.department || 'No Department'}
                        </p>
                        <div className="mt-auto">
                          <button
                            className="btn btn-primary w-100"
                            onClick={() => handleVote(candidate.id)}
                            disabled={voting}
                          >
                            {voting ? (
                              <>
                                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                Voting...
                              </>
                            ) : (
                              <>
                                <i className="bi bi-check-square me-2"></i>
                                Vote for {candidate.name}
                              </>
                            )}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Voting;
