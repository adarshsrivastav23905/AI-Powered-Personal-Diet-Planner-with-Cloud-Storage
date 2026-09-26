/**
 * Navbar Component
 * ==================
 * Responsive navigation bar with glassmorphism design.
 */

import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FiLogOut, FiUser, FiMenu, FiX } from 'react-icons/fi';
import { GiMeal } from 'react-icons/gi';
import { useState } from 'react';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <GiMeal size={28} />
        <span>NutriCloud AI</span>
      </Link>

      <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
        {menuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
      </button>

      <div className={`navbar-links ${menuOpen ? 'active' : ''}`}>
        {user ? (
          <>
            <Link to="/dashboard" onClick={() => setMenuOpen(false)}>Dashboard</Link>
            <Link to="/profile" onClick={() => setMenuOpen(false)}>Profile</Link>
            <Link to="/generate" onClick={() => setMenuOpen(false)}>Generate Plan</Link>
            <Link to="/plans" onClick={() => setMenuOpen(false)}>My Plans</Link>
            <Link to="/files" onClick={() => setMenuOpen(false)}>Cloud Files</Link>
            <div className="navbar-user">
              <FiUser size={16} />
              <span>{user.name}</span>
              <button onClick={handleLogout} className="btn-logout" title="Logout">
                <FiLogOut size={16} />
              </button>
            </div>
          </>
        ) : (
          <>
            <Link to="/login" onClick={() => setMenuOpen(false)}>Login</Link>
            <Link to="/register" onClick={() => setMenuOpen(false)} className="btn-nav-register">
              Get Started
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
