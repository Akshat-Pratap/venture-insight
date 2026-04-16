import React, { useState, useCallback } from 'react';
import FileUpload from '../components/FileUpload';
import ScoreGauge from '../components/ScoreGauge';
import SwotGrid from '../components/SwotCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { uploadPDF, analyzeStartup } from '../services/api';

function DashboardPage() {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [filename, setFilename] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [error, setError] = useState('');

  const handleFileSelect = useCallback((selectedFile) => {
    setFile(selectedFile);
    setExtractedText('');
    setAnalysisResult(null);
    setError('');
  }, []);

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a PDF file first.');
      return;
    }

    setLoading(true);
    setError('');
    setAnalysisResult(null);

    try {
      // Step 1: Upload and extract text
      setLoadingStep('Uploading and extracting text from PDF...');
      const uploadResult = await uploadPDF(file);
      setExtractedText(uploadResult.extracted_text);
      setFilename(uploadResult.filename);

      // Step 2: Run AI analysis
      setLoadingStep('Running AI analysis with Gemini... This may take 15-30 seconds.');
      const analysis = await analyzeStartup(
        uploadResult.extracted_text,
        uploadResult.filename
      );
      setAnalysisResult(analysis);

    } catch (err) {
      const message = err.response?.data?.detail || 'Analysis failed. Please try again.';
      setError(message);
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  const resetAnalysis = () => {
    setFile(null);
    setExtractedText('');
    setFilename('');
    setAnalysisResult(null);
    setError('');
  };

  return (
    <div className="page-container">
      <div className="page-header fade-in">
        <h1>Startup Analysis</h1>
        <p>Upload your pitch deck and get AI-powered insights, scoring, and SWOT analysis</p>
      </div>

      {/* Upload Section */}
      {!analysisResult && !loading && (
        <div className="fade-in-up" style={{ maxWidth: 640, margin: '0 auto' }}>
          <FileUpload onFileSelect={handleFileSelect} disabled={loading} />

          {error && (
            <div className="alert alert-error mt-lg" id="dashboard-error">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="15" y1="9" x2="9" y2="15" />
                <line x1="9" y1="9" x2="15" y2="15" />
              </svg>
              {error}
            </div>
          )}

          <div className="text-center mt-xl">
            <button
              className="btn btn-primary btn-lg"
              onClick={handleAnalyze}
              disabled={!file || loading}
              id="analyze-btn"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              Analyze Pitch Deck
            </button>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <LoadingSpinner
          message="Analyzing your startup pitch..."
          step={loadingStep}
        />
      )}

      {/* Results */}
      {analysisResult && !loading && (
        <div className="fade-in-up">
          {/* Action bar */}
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 'var(--space-lg)' }}>
            <button className="btn btn-secondary" onClick={resetAnalysis} id="new-analysis-btn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="1 4 1 10 7 10" />
                <path d="M3.51 15a9 9 0 102.13-9.36L1 10" />
              </svg>
              New Analysis
            </button>
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
              <ScoreGauge score={analysisResult.viability_score} />
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
              <ScoreBreakdown breakdown={analysisResult.score_breakdown} />
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
              <SwotGrid swotData={analysisResult.swot_analysis} />
            </div>

            {/* Detailed Analysis */}
            <div className="glass-card-static dashboard-full">
              <div className="section-title">
                <svg className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                  <polyline points="10 9 9 9 8 9" />
                </svg>
                Detailed Analysis
              </div>
              <div className="analysis-text" id="detailed-analysis">
                {analysisResult.detailed_analysis}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ─── Score Breakdown Sub-component ─────────────────────── */

function ScoreBreakdown({ breakdown }) {
  if (!breakdown) return <p className="text-muted">No breakdown available.</p>;

  const items = [
    { key: 'market_potential', label: 'Market Potential' },
    { key: 'team_strength', label: 'Team Strength' },
    { key: 'innovation', label: 'Innovation' },
    { key: 'financial_viability', label: 'Financial Viability' },
    { key: 'scalability', label: 'Scalability' },
  ];

  const getBarColor = (value) => {
    if (value >= 75) return 'linear-gradient(135deg, #10b981, #34d399)';
    if (value >= 55) return 'linear-gradient(135deg, #3b82f6, #60a5fa)';
    if (value >= 35) return 'linear-gradient(135deg, #f59e0b, #fbbf24)';
    return 'linear-gradient(135deg, #ef4444, #f87171)';
  };

  return (
    <div className="breakdown-grid">
      {items.map(({ key, label }) => {
        const value = breakdown[key] ?? 0;
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

      {breakdown.reasoning && (
        <div style={{ marginTop: 8 }}>
          <p className="breakdown-label" style={{ marginBottom: 4 }}>Reasoning</p>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            {breakdown.reasoning}
          </p>
        </div>
      )}
    </div>
  );
}

export default DashboardPage;
