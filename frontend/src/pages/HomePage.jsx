/**
 * Kosh Ticketing - HomePage
 * Landing page with hero, featured events, and categories
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { eventsAPI } from '../services/api';
import EventCard from '../components/events/EventCard';
import { LoadingPage, LoadingCard } from '../components/common/Loading';
import { 
  ArrowRight, Sparkles, Music, Theater, PartyPopper, 
  Trophy, Laugh, Palette, GraduationCap, ArrowUpRight 
} from 'lucide-react';
import { getCategoryConfig } from '../utils/helpers';

const categoryIcons = {
  concert: Music,
  theatre: Theater,
  festival: PartyPopper,
  sports: Trophy,
  comedy: Laugh,
  exhibition: Palette,
  workshop: GraduationCap,
};

const HomePage = () => {
  const { data: featuredData, isLoading: featuredLoading } = useQuery(
    'featured-events',
    eventsAPI.getFeatured
  );

  const { data: categoriesData, isLoading: categoriesLoading } = useQuery(
    'categories',
    eventsAPI.getCategories
  );

  const featuredEvents = featuredData?.data?.events || [];
  const categories = categoriesData?.data?.categories || [];

  return (
    <div className="min-h-screen bg-dark-900">
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-br from-kosh-950/80 via-dark-900/90 to-dark-900" />
          <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=1920')] bg-cover bg-center opacity-30" />
          {/* Animated gradient orbs */}
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-kosh-600/20 rounded-full blur-3xl animate-pulse-slow" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1.5s' }} />
        </div>

        <div className="relative max-w-7xl mx-auto section-padding w-full">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-kosh-500/10 border border-kosh-500/20 rounded-full mb-6">
              <Sparkles className="w-4 h-4 text-kosh-400" />
              <span className="text-sm font-medium text-kosh-400">Discover Amazing Events</span>
            </div>

            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black text-white leading-tight mb-6">
              Your Gateway to{' '}
              <span className="gradient-text">Unforgettable</span>{' '}
              Experiences
            </h1>

            <p className="text-lg sm:text-xl text-gray-400 mb-8 max-w-xl">
              Discover concerts, festivals, theatre, sports, and more. 
              Book tickets seamlessly and create memories that last a lifetime.
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <Link to="/events" className="btn-primary text-lg px-8 py-4 flex items-center justify-center gap-2">
                Explore Events
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link to="/register" className="btn-secondary text-lg px-8 py-4 flex items-center justify-center gap-2">
                Get Started
                <ArrowUpRight className="w-5 h-5" />
              </Link>
            </div>

            {/* Stats */}
            <div className="flex gap-8 mt-12 pt-8 border-t border-white/5">
              <div>
                <p className="text-3xl font-bold text-white">500+</p>
                <p className="text-sm text-gray-400">Events</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-white">50K+</p>
                <p className="text-sm text-gray-400">Happy Customers</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-white">100+</p>
                <p className="text-sm text-gray-400">Cities</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-16 border-t border-white/5">
        <div className="max-w-7xl mx-auto section-padding">
          <h2 className="text-2xl font-bold text-white mb-8">Browse by Category</h2>

          {categoriesLoading ? (
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4">
              {[...Array(7)].map((_, i) => (
                <div key={i} className="h-24 bg-white/5 rounded-xl animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4">
              {categories.map((cat) => {
                const Icon = categoryIcons[cat.id] || Sparkles;
                const config = getCategoryConfig(cat.id);
                return (
                  <Link
                    key={cat.id}
                    to={`/events?category=${cat.id}`}
                    className="group p-4 bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/10 rounded-xl transition-all text-center"
                  >
                    <div className={`w-10 h-10 mx-auto mb-3 rounded-lg bg-gradient-to-br ${config.color} flex items-center justify-center group-hover:scale-110 transition-transform`}>
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    <p className="text-sm font-medium text-white">{cat.name}</p>
                    <p className="text-xs text-gray-500 mt-1">{cat.count} events</p>
                  </Link>
                );
              })}
            </div>
          )}
        </div>
      </section>

      {/* Featured Events */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto section-padding">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-white">Featured Events</h2>
              <p className="text-gray-400 mt-1">Handpicked experiences just for you</p>
            </div>
            <Link to="/events?featured=true" className="text-kosh-400 hover:text-kosh-300 text-sm font-medium flex items-center gap-1">
              View All <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          {featuredLoading ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <LoadingCard key={i} />
              ))}
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {featuredEvents.map((event, index) => (
                <EventCard key={event.id} event={event} featured index={index} />
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto section-padding">
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-kosh-600 to-purple-700 p-8 sm:p-12 lg:p-16">
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
            <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />

            <div className="relative max-w-2xl">
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
                Ready to Host Your Own Event?
              </h2>
              <p className="text-lg text-white/80 mb-8">
                Join thousands of organizers who trust Kosh Ticketing to sell tickets, 
                manage attendees, and grow their events.
              </p>
              <Link to="/register" className="inline-flex items-center gap-2 px-8 py-4 bg-white text-kosh-700 font-bold rounded-xl hover:bg-gray-100 transition-all">
                Become an Organizer
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
