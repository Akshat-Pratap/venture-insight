import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ScoreGauge from '../components/ScoreGauge';
import SwotGrid from '../components/SwotCard';
import { getAnalysis } from '../services/api';

function AnalysisDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const data = await getAnalysis(id);
        setAnalysis(data);
      } catch (err) {
        setError('Failed to load analysis. It may not exist or you may not have access.');
      } finally {
        setLoading(false);
      }
    };
    fetchAnalysis();
  }, [id]);

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getBarColor = (value) => {
    if (value >= 75) return 'linear-gradient(135deg, #10b981, #34d399)';
    if (value >= 55) return 'linear-gradient(135deg, #3b82f6, #60a5fa)';
    if (value >= 35) return 'linear-gradient(135deg, #f59e0b, #fbbf24)';
    return 'linear-gradient(135deg, #ef4444, #f87171)';
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="spinner-overlay">
          <div className="spinner"></div>
          <div className="spinner-text">Loading analysis...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="alert alert-error">{error}</div>
        <button className="btn btn-secondary" onClick={() => navigate('/history')}>
          ← Back to History
        </button>
      </div>
    );
  }

  if (!analysis) return null;

  const breakdownItems = [
    { key: 'market_potential', label: 'Market Potential' },
    { key: 'team_strength', label: 'Team Strength' },
    { key: 'innovation', label: 'Innovation' },
    { key: 'financial_viability', label: 'Financial Viability' },
    { key: 'scalability', label: 'Scalability' },
  ];

  return (
    <div className="page-container">
      {/* Back button and header */}
      <div className="fade-in" style={{ marginBottom: 'var(--space-xl)' }}>
        <button
          className="btn btn-secondary"
          onClick={() => navigate('/history')}
          style={{ marginBottom: 'var(--space-lg)' }}
          id="back-to-history"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
          Back to History
        </button>
        <div className="page-header" style={{ marginBottom: 0 }}>
          <h1>{analysis.pitch_filename || 'Analysis Report'}</h1>
          <p>{formatDate(analysis.created_at)}</p>
        </div>
      </div>

      <div className="dashboard-grid stagger-children">
        {/* Score Gauge */}
        <div className="glass-card-static">
          <div className="section-title">
            <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
            Viability Score
          </div>
          <ScoreGauge score={analysis.viability_score} />
        </div>

        {/* Score Breakdown */}
        <div className="glass-card-static">
          <div className="section-title">
            <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="20" x2="18" y2="10" />
              <line x1="12" y1="20" x2="12" y2="4" />
              <line x1="6" y1="20" x2="6" y2="14" />
            </svg>
            Score Breakdown
          </div>
          {analysis.score_breakdown ? (
            <div className="breakdown-grid">
              {breakdownItems.map(({ key, label }) => {
                const value = analysis.score_breakdown[key] ?? 0;
                return (
                  <div className="breakdown-item" key={key}>
                    <div className="breakdown-header">
                      <span className="breakdown-label">{label}</span>
                      <span className="breakdown-value">{value}/100</span>
                    </div>
                    <div className="breakdown-bar">
                      <div
                        className="breakdown-bar-fill"
                        style={{
                          width: `${value}%`,
                          background: getBarColor(value),
                        }}
                      ></div>
                    </div>
                  </div>
                );
              })}
              {analysis.score_breakdown.reasoning && (
                <div style={{ marginTop: 8 }}>
                  <p className="breakdown-label" style={{ marginBottom: 4 }}>Reasoning</p>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                    {analysis.score_breakdown.reasoning}
                  </p>
                </div>
              )}
            </div>
          ) : (
            <p className="text-muted">No breakdown available.</p>
          )}
        </div>

        {/* SWOT Analysis */}
        <div className="glass-card-static dashboard-full">
          <div className="section-title">
            <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="12" y1="3" x2="12" y2="21" />
            </svg>
            SWOT Analysis
          </div>
          <SwotGrid swotData={analysis.swot_analysis} />
        </div>

        {/* Detailed Analysis */}
        <div className="glass-card-static dashboard-full">
          <div className="section-title">
            <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" />
              <line x1="16" y1="17" x2="8" y2="17" />
            </svg>
            Detailed Analysis
          </div>
          <div className="analysis-text" id="detail-analysis-text">
            {analysis.detailed_analysis}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AnalysisDetailPage;
