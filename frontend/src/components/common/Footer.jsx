/**
 * Kosh Ticketing - Footer Component
 * Modern footer with links and newsletter
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { Ticket, Mail, MapPin, Phone, Instagram, Twitter, Youtube, Facebook } from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    'Discover': ['Concerts', 'Theatre', 'Festivals', 'Sports', 'Comedy'],
    'Company': ['About Us', 'Careers', 'Press', 'Blog'],
    'Support': ['Help Center', 'Contact Us', 'Terms of Service', 'Privacy Policy'],
    'Organizers': ['Sell Tickets', 'Event Management', 'Pricing', 'Resources'],
  };

  const socialLinks = [
    { icon: Instagram, href: '#', label: 'Instagram' },
    { icon: Twitter, href: '#', label: 'Twitter' },
    { icon: Youtube, href: '#', label: 'YouTube' },
    { icon: Facebook, href: '#', label: 'Facebook' },
  ];

  return (
    <footer className="bg-dark-800 border-t border-white/5">
      {/* Newsletter */}
      <div className="section-padding py-12 border-b border-white/5">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-2xl font-bold mb-3">Never Miss an Event</h3>
          <p className="text-gray-400 mb-6">Subscribe to get notified about upcoming events and exclusive presales.</p>
          <div className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
            <div className="flex-1 relative">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="email"
                placeholder="Enter your email"
                className="w-full pl-12 pr-4 py-3 bg-dark-700 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-kosh-500 transition-all"
              />
            </div>
            <button className="btn-primary whitespace-nowrap">
              Subscribe
            </button>
          </div>
        </div>
      </div>

      {/* Main Footer */}
      <div className="section-padding py-12">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
            {/* Brand */}
            <div className="col-span-2 md:col-span-1">
              <Link to="/" className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-kosh-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Ticket className="w-4 h-4 text-white" />
                </div>
                <span className="font-bold text-lg">
                  <span className="gradient-text">Kosh</span>Ticketing
                </span>
              </Link>
              <p className="text-gray-400 text-sm mb-4">
                Your gateway to unforgettable live experiences. Discover, book, and enjoy the best events.
              </p>
              <div className="flex gap-3">
                {socialLinks.map((social) => (
                  <a
                    key={social.label}
                    href={social.href}
                    className="w-9 h-9 bg-white/5 hover:bg-kosh-500/20 rounded-lg flex items-center justify-center text-gray-400 hover:text-kosh-400 transition-all"
                    aria-label={social.label}
                  >
                    <social.icon className="w-4 h-4" />
                  </a>
                ))}
              </div>
            </div>

            {/* Links */}
            {Object.entries(footerLinks).map(([category, links]) => (
              <div key={category}>
                <h4 className="font-semibold text-white mb-4">{category}</h4>
                <ul className="space-y-2">
                  {links.map((link) => (
                    <li key={link}>
                      <Link to="#" className="text-gray-400 hover:text-kosh-400 text-sm transition-colors">
                        {link}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-white/5 section-padding py-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-gray-500 text-sm">
            © {currentYear} Kosh Ticketing. All rights reserved.
          </p>
          <div className="flex items-center gap-6 text-sm text-gray-500">
            <span className="flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              San Francisco, CA
            </span>
            <span className="flex items-center gap-2">
              <Phone className="w-4 h-4" />
              1-800-KOSH-TIX
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
