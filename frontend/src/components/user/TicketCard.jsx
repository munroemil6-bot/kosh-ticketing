/**
 * Kosh Ticketing - TicketCard Component
 * Digital ticket display with QR code and event details
 */

import React, { useState } from 'react';
import { formatDate, formatTime } from '../../utils/helpers';
import { QrCode, Calendar, MapPin, User, Download, ChevronDown, ChevronUp, CheckCircle } from 'lucide-react';

const TicketCard = ({ ticket }) => {
  const [expanded, setExpanded] = useState(false);
  const [showQR, setShowQR] = useState(false);

  return (
    <div className="glass-card overflow-hidden animate-fade-in">
      {/* Ticket Header */}
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-r from-kosh-600/20 to-purple-600/20" />
        <div className="relative p-5">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <span className="inline-block px-2.5 py-1 bg-kosh-500/20 rounded-lg text-xs font-medium text-kosh-400 mb-2">
                {ticket.ticket_tier_name}
              </span>
              <h3 className="text-lg font-bold text-white mb-1">{ticket.event_title}</h3>
              <div className="flex flex-wrap items-center gap-3 text-sm text-gray-400">
                <span className="flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5" />
                  {formatDate(ticket.event_date)}
                </span>
                <span className="flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5" />
                  {ticket.venue_name}
                </span>
              </div>
            </div>

            {/* Status Badge */}
            {ticket.is_checked_in ? (
              <span className="flex items-center gap-1 px-3 py-1.5 bg-emerald-500/20 rounded-lg text-xs font-semibold text-emerald-400">
                <CheckCircle className="w-3.5 h-3.5" />
                Checked In
              </span>
            ) : (
              <span className="px-3 py-1.5 bg-kosh-500/20 rounded-lg text-xs font-semibold text-kosh-400">
                Active
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Ticket Body */}
      <div className="px-5 pb-5">
        {/* Dashed Divider */}
        <div className="relative py-3">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-dashed border-white/10" />
          </div>
          <div className="relative flex justify-between">
            <div className="w-4 h-4 bg-dark-900 rounded-full -ml-7" />
            <div className="w-4 h-4 bg-dark-900 rounded-full -mr-7" />
          </div>
        </div>

        {/* Attendee Info */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-gray-400" />
            </div>
            <div>
              <p className="text-sm font-medium text-white">{ticket.first_name} {ticket.last_name}</p>
              <p className="text-xs text-gray-500">{ticket.email}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-xs text-gray-500">Ticket #</p>
            <p className="text-sm font-mono text-kosh-400">{ticket.ticket_number}</p>
          </div>
        </div>

        {/* QR Code Toggle */}
        <button
          onClick={() => setShowQR(!showQR)}
          className="w-full flex items-center justify-center gap-2 py-3 bg-white/5 hover:bg-white/10 rounded-xl transition-all text-sm font-medium text-gray-300"
        >
          <QrCode className="w-4 h-4" />
          {showQR ? 'Hide QR Code' : 'Show QR Code'}
          {showQR ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {/* QR Code Display */}
        {showQR && (
          <div className="mt-4 p-6 bg-white rounded-xl flex flex-col items-center animate-fade-in">
            <img
              src={ticket.qr_code}
              alt="Ticket QR Code"
              className="w-48 h-48"
            />
            <p className="mt-3 text-sm text-gray-600 font-mono">{ticket.ticket_number}</p>
            <p className="text-xs text-gray-400 mt-1">Present this at the venue entrance</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TicketCard;
