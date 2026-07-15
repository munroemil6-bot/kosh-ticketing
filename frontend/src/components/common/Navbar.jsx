/**
 * Kosh Ticketing - Navbar Component
 * Responsive navigation with mobile menu and auth state
 */

import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import { 
  Ticket, Search, Menu, X, User, LogOut, 
  Calendar, LayoutDashboard, ChevronDown 
}
from 'lucide-react';

const Navbar = () => {
  const { user, isAuthenticated, logout, isOrganizer } = useAuth();
  const { totalTickets } = useCart();
  const isCustomer = user?.role === 'customer';
  const navigate = useNavigate();
  const location = useLocation();

  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    setMobileMenuOpen(false);
    setUserMenuOpen(false);
  }, [location]);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navLinks = [
    { label: 'Events', path: '/events', icon: Calendar },
  ];

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled 
        ? 'bg-dark-900/90 backdrop-blur-xl border-b border-white/5 shadow-lg' 
        : 'bg-transparent'
    }`}>
      <div className="max-w-7xl mx-auto section-padding">
        <div className="flex items-center justify-between h-16 lg:h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-9 h-9 bg-gradient-to-br from-kosh-500 to-purple-600 rounded-xl flex items-center justify-center transform group-hover:scale-110 transition-transform">
              <Ticket className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold">
              <span className="gradient-text">Kosh</span>
              <span className="text-white">Ticketing</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                  location.pathname === link.path
                    ? 'text-kosh-400 bg-kosh-500/10'
                    : 'text-gray-300 hover:text-white hover:bg-white/5'
                }`}
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Right Section */}
          <div className="flex items-center gap-2">
            {/* Search Button */}
            <button 
              onClick={() => navigate('/events')}
              className="hidden sm:flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl text-gray-400 hover:text-white transition-all text-sm"
            >
              <Search className="w-4 h-4" />
              <span className="hidden lg:inline">Search events...</span>
            </button>

            {/* Cart Indicator */}
            {totalTickets > 0 && (
              <Link to="/checkout" className="relative p-2 hover:bg-white/5 rounded-xl transition-all">
                <Ticket className="w-5 h-5 text-kosh-400" />
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-kosh-500 rounded-full text-xs font-bold flex items-center justify-center">
                  {totalTickets}
                </span>
              </Link>
            )}

            {/* Auth Section */}
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setUserMenuOpen(!userMenuOpen)}
                  className="flex items-center gap-2 px-3 py-2 hover:bg-white/5 rounded-xl transition-all"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-kosh-500 to-purple-600 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-white" />
                  </div>
                  <span className="hidden lg:block text-sm font-medium text-gray-200">
                    {user?.first_name}
                  </span>
                  <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${userMenuOpen ? 'rotate-180' : ''}`} />
                </button>

                {/* Dropdown */}
                {userMenuOpen && (
                  <div className="absolute right-0 top-full mt-2 w-56 glass-card overflow-hidden animate-fade-in">
                    <div className="p-3 border-b border-white/5">
                      <p className="font-semibold text-white">{user?.full_name || user?.first_name + ' ' + user?.last_name}</p>
                      <p className="text-xs text-gray-400">{user?.email}</p>
                    </div>
                    <div className="p-1">
                      {isCustomer && (
                        <Link to="/my-tickets" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-300 hover:bg-white/5 hover:text-white transition-all">
                          <Ticket className="w-4 h-4" />
                          My Tickets
                        </Link>
                      )}
                      {isOrganizer && (
                        <Link to="/admin" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-300 hover:bg-white/5 hover:text-white transition-all">
                          <LayoutDashboard className="w-4 h-4" />
                          Dashboard
                        </Link>
                      )}
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-red-400 hover:bg-red-500/10 transition-all"
                      >
                        <LogOut className="w-4 h-4" />
                        Sign Out
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="hidden sm:flex items-center gap-2">
                <Link to="/login" className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white transition-all">
                  Sign In
                </Link>
                <Link to="/register" className="btn-primary text-sm py-2">
                  Get Started
                </Link>
              </div>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 hover:bg-white/5 rounded-xl transition-all"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-dark-900/95 backdrop-blur-xl border-t border-white/5 animate-slide-up">
          <div className="section-padding py-4 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className="flex items-center gap-3 px-4 py-3 rounded-xl text-gray-300 hover:bg-white/5 hover:text-white transition-all"
              >
                <link.icon className="w-5 h-5" />
                {link.label}
              </Link>
            ))}

            {!isAuthenticated && (
              <div className="pt-3 border-t border-white/5 space-y-2">
                <Link to="/login" className="block w-full text-center py-3 rounded-xl text-gray-300 hover:bg-white/5 transition-all">
                  Sign In
                </Link>
                <Link to="/register" className="block w-full text-center btn-primary">
                  Get Started
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
