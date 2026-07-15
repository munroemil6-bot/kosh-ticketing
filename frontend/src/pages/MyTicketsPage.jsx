import React from 'react';
import { Link, Navigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { useAuth } from '../context/AuthContext';
import { ticketsAPI } from '../services/api';
import TicketCard from '../components/user/TicketCard';
import { LoadingPage } from '../components/common/Loading';
import { Ticket, AlertCircle } from 'lucide-react';

const MyTicketsPage = () => {
  const { user } = useAuth();
  const { data, isLoading, error } = useQuery('my-tickets', ticketsAPI.getMyTickets, {
    enabled: user?.role === 'customer',
  });

  if (user?.role !== 'customer') {
    return <Navigate to="/admin" replace />;
  }

  const tickets = data?.data?.tickets || [];

  if (isLoading) return <LoadingPage />;

  return (
    <div className="min-h-screen bg-dark-900 pt-24 pb-12">
      <div className="max-w-3xl mx-auto section-padding">
        <div className="flex items-center gap-3 mb-8">
          <Ticket className="w-6 h-6 text-kosh-400" />
          <h1 className="text-3xl font-bold text-white">My Tickets</h1>
        </div>

        {error ? (
          <div className="glass-card p-8 text-center">
            <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-3" />
            <p className="text-red-400">Failed to load tickets</p>
          </div>
        ) : tickets.length > 0 ? (
          <div className="space-y-6">
            {tickets.map(ticket => (
              <TicketCard key={ticket.id} ticket={ticket} />
            ))}
          </div>
        ) : (
          <div className="glass-card p-12 text-center">
            <Ticket className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white mb-2">No Tickets Yet</h3>
            <p className="text-gray-400 mb-6">Your purchased tickets will appear here once checkout is complete.</p>
            <Link to="/events" className="btn-primary">Buy Tickets</Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default MyTicketsPage;
