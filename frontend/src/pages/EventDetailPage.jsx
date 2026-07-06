import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { eventsAPI } from '../services/api';
import { useCart } from '../context/CartContext';
import TicketSelector from '../components/events/TicketSelector';
import EventCard from '../components/events/EventCard';
import { LoadingPage } from '../components/common/Loading';
import {
  Calendar, MapPin, Clock, Share2, Heart,
  ArrowRight, AlertTriangle
} from 'lucide-react';
import { formatDateTime, formatTime, getCategoryConfig, getDaysUntil } from '../utils/helpers';

const EventDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { setEvent, clearCart } = useCart();

  const { data, isLoading } = useQuery(
    ['event', id],
    () => eventsAPI.getEvent(id)
  );

  const { data: relatedData } = useQuery(
    ['related', id],
    () => eventsAPI.getRelated(id),
    { enabled: !!data }
  );

  const event = data?.data?.event;
  const relatedEvents = relatedData?.data?.events || [];

  useEffect(() => {
    if (event) {
      clearCart();
      setEvent(event);
    }
    return () => clearCart();
  }, [event, setEvent, clearCart]);

  if (isLoading) return <LoadingPage />;
  if (!event) return <div className="min-h-screen flex items-center justify-center text-gray-500">Event not found</div>;

  const category = getCategoryConfig(event.category);
  const daysUntil = getDaysUntil(event.start_date);

  const handleContinueCheckout = () => {
    navigate('/checkout');
  };

  return (
    <div className="min-h-screen bg-dark-900 pt-16">
      {/* Hero Banner */}
      <div className="relative h-[50vh] min-h-[400px]">
        <img
          src={event.banner_image}
          alt={event.title}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark-900 via-dark-900/60 to-transparent" />

        <div className="absolute bottom-0 left-0 right-0 section-padding pb-8">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center gap-2 mb-4">
              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${category.bg} ${category.text}`}>
                {category.label}
              </span>
              {event.is_featured && (
                <span className="px-3 py-1 bg-kosh-500/20 rounded-full text-xs font-semibold text-kosh-400">
                  Featured
                </span>
              )}
              {daysUntil && (
                <span className="px-3 py-1 bg-white/10 rounded-full text-xs text-white">
                  {daysUntil}
                </span>
              )}
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-3">
              {event.title}
            </h1>
            {event.subtitle && (
              <p className="text-xl text-gray-300">{event.subtitle}</p>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto section-padding py-12">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Quick Info */}
            <div className="glass-card p-6">
              <div className="grid sm:grid-cols-2 gap-4">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-kosh-500/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Calendar className="w-5 h-5 text-kosh-400" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Date & Time</p>
                    <p className="font-medium text-white">{formatDateTime(event.start_date)}</p>
                    {event.doors_open && (
                      <p className="text-sm text-gray-500">Doors: {formatTime(event.doors_open)}</p>
                    )}
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-kosh-500/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <MapPin className="w-5 h-5 text-kosh-400" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Venue</p>
                    <p className="font-medium text-white">{event.venue_name}</p>
                    <p className="text-sm text-gray-500">
                      {event.venue_address}{event.venue_city && `, ${event.venue_city}`}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Description */}
            <div className="glass-card p-6">
              <h2 className="text-xl font-bold text-white mb-4">About This Event</h2>
              {event.rich_description ? (
                <div
                  className="prose prose-invert max-w-none"
                  dangerouslySetInnerHTML={{ __html: event.rich_description }}
                />
              ) : (
                <p className="text-gray-300 leading-relaxed">{event.description}</p>
              )}
            </div>

            {/* Tags */}
            {event.tags?.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {event.tags.map(tag => (
                  <span key={tag} className="px-3 py-1 bg-white/5 rounded-full text-sm text-gray-400">
                    #{tag}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Sidebar - Ticket Selection */}
          <div className="lg:col-span-1">
            <div className="sticky top-24">
              {event.is_sold_out ? (
                <div className="glass-card p-6 text-center">
                  <AlertTriangle className="w-12 h-12 text-red-400 mx-auto mb-3" />
                  <h3 className="text-lg font-bold text-red-400 mb-2">Sold Out</h3>
                  <p className="text-gray-400 text-sm">This event is completely sold out.</p>
                </div>
              ) : (
                <TicketSelector event={event} onContinue={handleContinueCheckout} />
              )}
            </div>
          </div>
        </div>

        {/* Related Events */}
        {relatedEvents.length > 0 && (
          <div className="mt-16">
            <h2 className="text-2xl font-bold text-white mb-6">You Might Also Like</h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {relatedEvents.map(event => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EventDetailPage;
