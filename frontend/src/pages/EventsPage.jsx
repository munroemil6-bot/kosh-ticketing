import React, { useState, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { eventsAPI } from '../services/api';
import EventCard from '../components/events/EventCard';
import SearchFilter from '../components/events/SearchFilter';
import { LoadingCard } from '../components/common/Loading';

const EventsPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const [filters, setFilters] = useState({
    category: searchParams.get('category') || '',
    search: searchParams.get('search') || '',
    city: '',
    date_from: '',
    date_to: '',
    page: 1,
  });

  const { data, isLoading } = useQuery(
    ['events', filters],
    () => eventsAPI.getEvents(filters),
    { keepPreviousData: true }
  );

  const { data: categoriesData } = useQuery('categories', eventsAPI.getCategories);

  const handleSearch = useCallback((search) => {
    setFilters(prev => ({ ...prev, search, page: 1 }));
  }, []);

  const handleFilterChange = useCallback((newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }));
  }, []);

  const handlePageChange = (page) => {
    setFilters(prev => ({ ...prev, page }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const events = data?.data?.events || [];
  const pagination = data?.data?.pagination;
  const categories = categoriesData?.data?.categories || [];

  return (
    <div className="min-h-screen bg-dark-900 pt-24 pb-12">
      <div className="max-w-7xl mx-auto section-padding">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Discover Events</h1>
          <p className="text-gray-400">Find your next unforgettable experience</p>
        </div>
        <div className="mb-8">
          <SearchFilter
            categories={categories}
            filters={filters}
            onSearch={handleSearch}
            onFilterChange={handleFilterChange}
          />
        </div>

        <div className="flex items-center justify-between mb-6">
          <p className="text-sm text-gray-400">
            {isLoading ? 'Loading...' : `${pagination?.total || 0} events found`}
          </p>
        </div>

        {isLoading ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(12)].map((_, i) => (
              <LoadingCard key={i} />
            ))}
          </div>
        ) : events.length > 0 ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {events.map((event, index) => (
              <EventCard key={event.id} event={event} index={index} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <p className="text-gray-500 text-lg">No events found matching your criteria</p>
            <button
              onClick={() => handleFilterChange({ category: '', search: '', city: '' })}
              className="mt-4 text-kosh-400 hover:text-kosh-300"
            >
              Clear all filters
            </button>
          </div>
        )}

        {pagination && pagination.pages > 1 && (
          <div className="flex items-center justify-center gap-2 mt-12">
            <button
              onClick={() => handlePageChange(filters.page - 1)}
              disabled={!pagination.has_prev}
              className="p-2 rounded-lg bg-white/5 hover:bg-white/10 disabled:opacity-30 transition-all"
            >
              Previous
            </button>
            {[...Array(pagination.pages)].map((_, i) => (
              <button
                key={i}
                onClick={() => handlePageChange(i + 1)}
                className={`w-10 h-10 rounded-lg font-medium transition-all ${
                  filters.page === i + 1
                    ? 'bg-kosh-500 text-white'
                    : 'bg-white/5 text-gray-400 hover:bg-white/10'
                }`}
              >
                {i + 1}
              </button>
            ))}
            <button
              onClick={() => handlePageChange(filters.page + 1)}
              disabled={!pagination.has_next}
              className="p-2 rounded-lg bg-white/5 hover:bg-white/10 disabled:opacity-30 transition-all"
            >
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default EventsPage;
