/**
 * Kosh Ticketing - AdminDashboard Component
 * Organizer/Admin dashboard with stats, events, and management
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { adminAPI } from '../../services/api';
import { 
  Calendar, Ticket, DollarSign, TrendingUp, 
  Users, Eye, Plus, BarChart3, ArrowUpRight 
} from 'lucide-react';
import { formatCurrency } from '../../utils/helpers';
import { LoadingPage } from '../common/Loading';

const StatCard = ({ title, value, icon: Icon, trend, color }) => (
  <div className="glass-card p-5">
    <div className="flex items-start justify-between mb-4">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${color}`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
      {trend && (
        <span className="flex items-center gap-1 text-xs font-medium text-emerald-400">
          <ArrowUpRight className="w-3 h-3" />
          {trend}
        </span>
      )}
    </div>
    <p className="text-2xl font-bold text-white">{value}</p>
    <p className="text-sm text-gray-400 mt-1">{title}</p>
  </div>
);

const AdminDashboard = () => {
  const { data, isLoading, error } = useQuery('dashboard', adminAPI.getDashboard, {
    retry: 1,
  });

  if (isLoading) return <LoadingPage />;
  if (error) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <p className="text-red-400 mb-2">Failed to load dashboard</p>
        <button onClick={() => window.location.reload()} className="text-kosh-400 hover:underline">
          Retry
        </button>
      </div>
    </div>
  );

  const stats = data?.data?.stats || {};
  const recentOrders = data?.data?.recent_orders || [];
  const eventsPerformance = data?.data?.events_performance || [];

  return (
    <div className="min-h-screen bg-dark-900 pt-24 pb-12">
      <div className="max-w-7xl mx-auto section-padding">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Dashboard</h1>
            <p className="text-gray-400 mt-1">Manage your events and track performance</p>
          </div>
          <Link to="/admin/events/create" className="btn-primary flex items-center gap-2">
            <Plus className="w-4 h-4" />
            Create Event
          </Link>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard
            title="Total Events"
            value={stats.total_events}
            icon={Calendar}
            color="bg-blue-500/20"
          />
          <StatCard
            title="Total Orders"
            value={stats.total_orders}
            icon={Ticket}
            color="bg-kosh-500/20"
            trend="+12%"
          />
          <StatCard
            title="Revenue"
            value={formatCurrency(stats.total_revenue)}
            icon={DollarSign}
            color="bg-emerald-500/20"
            trend="+8%"
          />
          <StatCard
            title="Tickets Sold"
            value={stats.total_tickets_sold}
            icon={TrendingUp}
            color="bg-violet-500/20"
          />
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Events Performance */}
          <div className="lg:col-span-2">
            <div className="glass-card p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-white">Events Performance</h2>
                <Link to="/admin/events" className="text-sm text-kosh-400 hover:text-kosh-300 flex items-center gap-1">
                  View All <ArrowUpRight className="w-4 h-4" />
                </Link>
              </div>

              <div className="space-y-4">
                {eventsPerformance.map((event) => (
                  <div key={event.id} className="flex items-center gap-4 p-4 bg-dark-700/50 rounded-xl">
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-white truncate">{event.title}</h4>
                      <div className="flex items-center gap-4 mt-1 text-xs text-gray-400">
                        <span>{event.tickets_sold} / {event.capacity} sold</span>
                        <span>{formatCurrency(event.revenue)} revenue</span>
                      </div>
                    </div>
                    <div className="w-32">
                      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-kosh-500 to-purple-500 rounded-full transition-all"
                          style={{ width: `${Math.min((event.tickets_sold / event.capacity) * 100, 100)}%` }}
                        />
                      </div>
                      <p className="text-xs text-gray-500 mt-1 text-right">
                        {Math.round((event.tickets_sold / event.capacity) * 100)}%
                      </p>
                    </div>
                    <Link
                      to={`/admin/events/${event.id}`}
                      className="p-2 hover:bg-white/5 rounded-lg transition-all"
                    >
                      <Eye className="w-4 h-4 text-gray-400" />
                    </Link>
                  </div>
                ))}

                {eventsPerformance.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <Calendar className="w-12 h-12 mx-auto mb-3 opacity-30" />
                    <p>No events yet. Create your first event!</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Recent Orders */}
          <div>
            <div className="glass-card p-6">
              <h2 className="text-lg font-bold text-white mb-6">Recent Orders</h2>
              <div className="space-y-3">
                {recentOrders.map((order) => (
                  <div key={order.id} className="p-3 bg-dark-700/50 rounded-xl">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-mono text-kosh-400">{order.order_number}</span>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        order.status === 'paid' ? 'bg-emerald-500/20 text-emerald-400' :
                        order.status === 'pending' ? 'bg-amber-500/20 text-amber-400' :
                        'bg-red-500/20 text-red-400'
                      }`}>
                        {order.status}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500">
                      {order.total_tickets} tickets • {formatCurrency(order.total)}
                    </p>
                  </div>
                ))}

                {recentOrders.length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <Ticket className="w-10 h-10 mx-auto mb-2 opacity-30" />
                    <p className="text-sm">No orders yet</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
