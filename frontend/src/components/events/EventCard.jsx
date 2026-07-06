/**
 * Kosh Ticketing - EventCard Component
 * Reusable event card with hover effects and quick actions
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { Calendar, MapPin, Ticket, ArrowRight } from 'lucide-react';
import { formatDate, formatCurrency, getCategoryConfig, getEventStatus, getDaysUntil } from '../../utils/helpers';

const EventCard = ({ event, featured = false, index = 0 }) => {
  const category = getCategoryConfig(event.category);
  const status = getEventStatus(event);
  const daysUntil = getDaysUntil(event.start_date);

  if (featured) {
    return (
      <Link
        to={`/events/${event.id}`}
        className="group relative overflow-hidden rounded-2xl bg-dark-800 border border-white/5 hover:border-kosh-500/30 transition-all duration-500"
        style={{ animationDelay: `${index * 100}ms` }}
      >
        <div className="relative aspect-[16/9] overflow-hidden">
          <img
            src={event.banner_image || event.thumbnail_image || '/placeholder-event.jpg'}
            alt={event.title}
            className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-dark-900 via-dark-900/40 to-transparent" />

          {/* Badges */}
          <div className="absolute top-4 left-4 flex gap-2">
            {event.is_featured && (
              <span className="px-3 py-1 bg-kosh-500/90 backdrop-blur-sm rounded-full text-xs font-semibold text-white">
                Featured
              </span>
            )}
            <span className={`px-3 py-1 backdrop-blur-sm rounded-full text-xs font-semibold ${status.color}`}>
              {status.label}
            </span>
          </div>

          {/* Days Until */}
          {daysUntil && (
            <div className="absolute top-4 right-4 px-3 py-1.5 bg-dark-900/80 backdrop-blur-sm rounded-lg">
              <span className="text-xs font-semibold text-kosh-400">{daysUntil}</span>
            </div>
          )}

          {/* Bottom Info */}
          <div className="absolute bottom-0 left-0 right-0 p-5">
            <div className="flex items-center gap-2 mb-2">
              <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${category.bg} ${category.text}`}>
                {category.label}
              </span>
              {event.age_restriction && (
                <span className="px-2 py-0.5 bg-white/10 rounded-md text-xs text-gray-300">
                  {event.age_restriction}
                </span>
              )}
            </div>
            <h3 className="text-xl font-bold text-white mb-1 group-hover:text-kosh-300 transition-colors line-clamp-2">
              {event.title}
            </h3>
            {event.subtitle && (
              <p className="text-sm text-gray-400 line-clamp-1 mb-3">{event.subtitle}</p>
            )}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4 text-sm text-gray-400">
                <span className="flex items-center gap-1.5">
                  <Calendar className="w-4 h-4" />
                  {formatDate(event.start_date)}
                </span>
                <span className="flex items-center gap-1.5">
                  <MapPin className="w-4 h-4" />
                  {event.venue_city}
                </span>
              </div>
              <div className="flex items-center gap-2">
                {event.lowest_price && (
                  <span className="text-lg font-bold text-white">
                    {formatCurrency(event.lowest_price)}
                  </span>
                )}
                <ArrowRight className="w-5 h-5 text-kosh-400 transform group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </div>
        </div>
      </Link>
    );
  }

  // Standard card
  return (
    <Link
      to={`/events/${event.id}`}
      className="group block glass-card overflow-hidden hover:border-kosh-500/30 transition-all duration-300"
    >
      <div className="relative aspect-[4/3] overflow-hidden">
        <img
          src={event.thumbnail_image || event.banner_image || '/placeholder-event.jpg'}
          alt={event.title}
          className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark-900/60 to-transparent" />

        <div className="absolute top-3 left-3 flex gap-2">
          <span className={`px-2.5 py-1 rounded-lg text-xs font-semibold ${category.bg} ${category.text}`}>
            {category.label}
          </span>
        </div>

        {event.is_sold_out && (
          <div className="absolute inset-0 bg-dark-900/70 flex items-center justify-center backdrop-blur-sm">
            <span className="px-4 py-2 bg-red-500/20 border border-red-500/30 rounded-xl text-red-400 font-bold text-lg">
              Sold Out
            </span>
          </div>
        )}
      </div>

      <div className="p-4">
        <h3 className="font-bold text-white mb-1 group-hover:text-kosh-300 transition-colors line-clamp-1">
          {event.title}
        </h3>
        <p className="text-sm text-gray-400 mb-3 line-clamp-1">{event.venue_name}</p>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 text-xs text-gray-500">
            <span className="flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5" />
              {formatDate(event.start_date, 'MMM d')}
            </span>
            <span className="flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5" />
              {event.venue_city}
            </span>
          </div>

          {event.lowest_price ? (
            <span className="text-sm font-bold text-white">
              {formatCurrency(event.lowest_price)}
            </span>
          ) : (
            <span className="text-xs text-gray-500">Free</span>
          )}
        </div>
      </div>
    </Link>
  );
};

export default EventCard;
