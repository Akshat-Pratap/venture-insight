import React, { useMemo } from 'react';

function ScoreGauge({ score }) {
  const numericScore = Number(score) || 0;
  const circumference = 2 * Math.PI * 85; // radius = 85
  const dashoffset = circumference - (numericScore / 100) * circumference;

  const { color, label, className } = useMemo(() => {
    if (numericScore >= 75) return { color: '#10b981', label: 'Excellent', className: 'excellent' };
    if (numericScore >= 55) return { color: '#3b82f6', label: 'Good', className: 'good' };
    if (numericScore >= 35) return { color: '#f59e0b', label: 'Average', className: 'average' };
    return { color: '#ef4444', label: 'Poor', className: 'poor' };
  }, [numericScore]);

  return (
    <div className="score-gauge-container fade-in-up" id="score-gauge">
      <div className="score-gauge">
        <svg viewBox="0 0 200 200">
          <circle
            className="track"
            cx="100"
            cy="100"
            r="85"
          />
          <circle
            className="progress"
            cx="100"
            cy="100"
            r="85"
            stroke={color}
            strokeDasharray={circumference}
            strokeDashoffset={dashoffset}
            style={{ filter: `drop-shadow(0 0 8px ${color}40)` }}
          />
        </svg>
        <div className="score-value">
          <div className="number" style={{ color }}>{Math.round(numericScore)}</div>
          <div className="label">Viability</div>
        </div>
      </div>
      <span className={`score-label ${className}`}>{label}</span>
    </div>
  );
}

export default ScoreGauge;
