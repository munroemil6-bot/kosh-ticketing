/**
 * Kosh Ticketing - SearchFilter Component
 * Event search, category filters, and sort options
 */

import React, { useState, useCallback } from 'react';
import { Search, SlidersHorizontal, X, Calendar, MapPin } from 'lucide-react';
import { debounce } from '../../utils/helpers';

const SearchFilter = ({ categories, onSearch, onFilterChange, filters }) => {
  const [searchQuery, setSearchQuery] = useState(filters.search || '');
  const [showFilters, setShowFilters] = useState(false);

  const debouncedSearch = useCallback(
    debounce((value) => {
      onSearch(value);
    }, 300),
    [onSearch]
  );

  const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    debouncedSearch(value);
  };

  const handleCategoryClick = (categoryId) => {
    onFilterChange({ category: filters.category === categoryId ? '' : categoryId });
  };

  const clearFilters = () => {
    setSearchQuery('');
    onFilterChange({ category: '', search: '', city: '', date_from: '', date_to: '' });
  };

  const hasActiveFilters = filters.category || filters.city || filters.date_from || filters.search;

  return (
    <div className="space-y-4">
      {/* Search Bar */}
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={handleSearchChange}
            placeholder="Search events, artists, venues..."
            className="w-full pl-12 pr-4 py-3.5 bg-dark-700 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-kosh-500 focus:ring-1 focus:ring-kosh-500 transition-all"
          />
          {searchQuery && (
            <button
              onClick={() => { setSearchQuery(''); onSearch(''); }}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        <button
          onClick={() => setShowFilters(!showFilters)}
          className={`flex items-center gap-2 px-4 py-3.5 rounded-xl border transition-all ${
            showFilters || hasActiveFilters
              ? 'bg-kosh-500/10 border-kosh-500/30 text-kosh-400'
              : 'bg-dark-700 border-white/10 text-gray-400 hover:text-white'
          }`}
        >
          <SlidersHorizontal className="w-5 h-5" />
          <span className="hidden sm:inline text-sm font-medium">Filters</span>
          {hasActiveFilters && (
            <span className="w-2 h-2 bg-kosh-500 rounded-full" />
          )}
        </button>
      </div>

      {/* Category Pills */}
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
        <button
          onClick={() => handleCategoryClick('')}
          className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
            !filters.category
              ? 'bg-kosh-500 text-white'
              : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
          }`}
        >
          All Events
        </button>
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => handleCategoryClick(cat.id)}
            className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
              filters.category === cat.id
                ? 'bg-kosh-500 text-white'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
            }`}
          >
            {cat.name}
            <span className="ml-1.5 text-xs opacity-70">({cat.count})</span>
          </button>
        ))}
      </div>

      {/* Advanced Filters */}
      {showFilters && (
        <div className="glass-card p-4 animate-fade-in space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1.5">City</label>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                  type="text"
                  value={filters.city || ''}
                  onChange={(e) => onFilterChange({ city: e.target.value })}
                  placeholder="Any city"
                  className="w-full pl-10 pr-4 py-2.5 bg-dark-700 border border-white/10 rounded-lg text-sm text-white placeholder-gray-500 focus:outline-none focus:border-kosh-500 transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-1.5">From Date</label>
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                  type="date"
                  value={filters.date_from || ''}
                  onChange={(e) => onFilterChange({ date_from: e.target.value })}
                  className="w-full pl-10 pr-4 py-2.5 bg-dark-700 border border-white/10 rounded-lg text-sm text-white focus:outline-none focus:border-kosh-500 transition-all [color-scheme:dark]"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-1.5">To Date</label>
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                  type="date"
                  value={filters.date_to || ''}
                  onChange={(e) => onFilterChange({ date_to: e.target.value })}
                  className="w-full pl-10 pr-4 py-2.5 bg-dark-700 border border-white/10 rounded-lg text-sm text-white focus:outline-none focus:border-kosh-500 transition-all [color-scheme:dark]"
                />
              </div>
            </div>
          </div>

          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="text-sm text-kosh-400 hover:text-kosh-300 transition-colors"
            >
              Clear all filters
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchFilter;
