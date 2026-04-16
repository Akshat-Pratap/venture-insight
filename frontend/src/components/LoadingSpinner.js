import React from 'react';

function LoadingSpinner({ message, step }) {
  return (
    <div className="spinner-overlay fade-in" id="loading-spinner">
      <div className="spinner"></div>
      <div className="spinner-text">
        {message || 'Processing...'}
        {step && <span className="spinner-step">{step}</span>}
      </div>
      <div className="progress-bar-container">
        <div className="progress-bar">
          <div className="progress-bar-fill"></div>
        </div>
      </div>
    </div>
  );
}

export default LoadingSpinner;
