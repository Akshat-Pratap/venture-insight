import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAnalyses } from '../services/api';

function HistoryPage() {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getAnalyses();
        setAnalyses(data);
      } catch (err) {
        setError('Failed to load analysis history.');
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const getScoreColor = (score) => {
    if (score >= 75) return '#10b981';
    if (score >= 55) return '#3b82f6';
    if (score >= 35) return '#f59e0b';
    return '#ef4444';
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="page-container">
      <div className="page-header fade-in">
        <h1>Analysis History</h1>
        <p>View your past startup analysis reports</p>
      </div>

      {loading && (
        <div className="spinner-overlay">
          <div className="spinner"></div>
          <div className="spinner-text">Loading history...</div>
        </div>
      )}

      {error && (
        <div className="alert alert-error" id="history-error">
          {error}
        </div>
      )}

      {!loading && !error && analyses.length === 0 && (
        <div className="empty-state fade-in">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3>No analyses yet</h3>
          <p>Upload a pitch deck on the Dashboard to get started.</p>
          <button
            className="btn btn-primary mt-lg"
            onClick={() => navigate('/dashboard')}
            id="go-to-dashboard"
          >
            Go to Dashboard
          </button>
        </div>
      )}

      {!loading && analyses.length > 0 && (
        <div className="history-list stagger-children" id="history-list">
          {analyses.map((analysis) => (
            <div
              key={analysis.id}
              className="history-item"
              onClick={() => navigate(`/analysis/${analysis.id}`)}
              id={`history-item-${analysis.id}`}
            >
              <div
                className="history-score"
                style={{ color: getScoreColor(analysis.score) }}
              >
                {analysis.score != null ? Math.round(analysis.score) : '—'}
              </div>
              <div className="history-info">
                <div className="history-filename">
                  {analysis.pitch_filename || 'Untitled Analysis'}
                </div>
                <div className="history-date">
                  {formatDate(analysis.created_at)}
                </div>
              </div>
              <div className="history-arrow">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="9 18 15 12 9 6" />
                </svg>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default HistoryPage;
