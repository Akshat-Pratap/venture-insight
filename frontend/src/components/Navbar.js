import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../App';

function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <nav className="navbar" id="main-navbar">
      <Link to="/dashboard" className="navbar-brand">
        <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="logo-grad" x1="0" y1="0" x2="28" y2="28">
              <stop offset="0%" stopColor="#06b6d4" />
              <stop offset="50%" stopColor="#6366f1" />
              <stop offset="100%" stopColor="#a855f7" />
            </linearGradient>
          </defs>
          <path d="M14 2L26 8V20L14 26L2 20V8L14 2Z" stroke="url(#logo-grad)" strokeWidth="2" fill="none"/>
          <path d="M14 8L20 11V17L14 20L8 17V11L14 8Z" fill="url(#logo-grad)" opacity="0.6"/>
          <circle cx="14" cy="14" r="2.5" fill="url(#logo-grad)"/>
        </svg>
        VENTURE INSIGHT
      </Link>
      <div className="navbar-links">
        <Link
          to="/dashboard"
          className={location.pathname === '/dashboard' ? 'active' : ''}
          id="nav-dashboard"
        >
          Dashboard
        </Link>
        <Link
          to="/history"
          className={location.pathname === '/history' ? 'active' : ''}
          id="nav-history"
        >
          History
        </Link>
        {user && (
          <span className="nav-user-email">{user.email}</span>
        )}
        <button onClick={logout} id="nav-logout">
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
