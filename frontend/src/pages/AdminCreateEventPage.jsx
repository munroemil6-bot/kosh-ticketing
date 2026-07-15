import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventsAPI } from '../services/api';
import { CalendarPlus, Loader2 } from 'lucide-react';

const initialForm = {
  title: '',
  subtitle: '',
  description: '',
  category: 'concert',
  start_date: '',
  venue_name: '',
  venue_address: '',
  venue_city: '',
  venue_country: '',
  banner_image: '',
  thumbnail_image: '',
  tier_name: 'General Admission',
  tier_price: '50',
  tier_quantity: '100',
  tier_description: 'Standard entry',
};

const AdminCreateEventPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [form, setForm] = useState(initialForm);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const payload = {
        title: form.title,
        subtitle: form.subtitle,
        description: form.description,
        category: form.category,
        start_date: new Date(form.start_date).toISOString(),
        venue_name: form.venue_name,
        venue_address: form.venue_address,
        venue_city: form.venue_city,
        venue_country: form.venue_country,
        banner_image: form.banner_image || undefined,
        thumbnail_image: form.thumbnail_image || undefined,
        organizer_name: `${user?.first_name || ''} ${user?.last_name || ''}`.trim() || user?.email,
        is_public: true,
        ticket_tiers: [{
          name: form.tier_name,
          description: form.tier_description,
          price: Number(form.tier_price),
          quantity_total: Number(form.tier_quantity),
          min_per_order: 1,
          max_per_order: 10,
          sale_start: new Date().toISOString(),
        }],
      };

      await eventsAPI.createEvent(payload);
      navigate('/admin');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create event');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-900 pt-24 pb-12">
      <div className="max-w-4xl mx-auto section-padding">
        <div className="flex items-center gap-3 mb-8">
          <CalendarPlus className="w-6 h-6 text-kosh-400" />
          <div>
            <h1 className="text-3xl font-bold text-white">Create Event</h1>
            <p className="text-gray-400">Publish a new event and set its first ticket tier.</p>
          </div>
        </div>

        {error && (
          <div className="mb-6 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="glass-card p-6 space-y-6">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Title</label>
              <input name="title" value={form.title} onChange={handleChange} required className="input-field" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Subtitle</label>
              <input name="subtitle" value={form.subtitle} onChange={handleChange} className="input-field" />
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Description</label>
            <textarea name="description" value={form.description} onChange={handleChange} required rows="4" className="input-field" />
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Category</label>
              <select name="category" value={form.category} onChange={handleChange} className="input-field">
                <option value="concert">Concert</option>
                <option value="theatre">Theatre</option>
                <option value="festival">Festival</option>
                <option value="sports">Sports</option>
                <option value="comedy">Comedy</option>
                <option value="exhibition">Exhibition</option>
                <option value="workshop">Workshop</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Start date</label>
              <input name="start_date" value={form.start_date} onChange={handleChange} type="datetime-local" required className="input-field" />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Venue name</label>
              <input name="venue_name" value={form.venue_name} onChange={handleChange} required className="input-field" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Venue address</label>
              <input name="venue_address" value={form.venue_address} onChange={handleChange} className="input-field" />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">City</label>
              <input name="venue_city" value={form.venue_city} onChange={handleChange} className="input-field" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Country</label>
              <input name="venue_country" value={form.venue_country} onChange={handleChange} className="input-field" />
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Tier name</label>
              <input name="tier_name" value={form.tier_name} onChange={handleChange} className="input-field" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Price</label>
              <input name="tier_price" value={form.tier_price} onChange={handleChange} type="number" min="0" className="input-field" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Quantity</label>
              <input name="tier_quantity" value={form.tier_quantity} onChange={handleChange} type="number" min="1" className="input-field" />
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Tier description</label>
            <input name="tier_description" value={form.tier_description} onChange={handleChange} className="input-field" />
          </div>

          <div className="flex justify-end">
            <button type="submit" disabled={isLoading} className="btn-primary flex items-center gap-2">
              {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Create Event'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdminCreateEventPage;
