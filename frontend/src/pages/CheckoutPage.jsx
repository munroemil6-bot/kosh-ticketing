import React from 'react';
import { Navigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import CheckoutFlow from '../components/checkout/CheckoutFlow';
import { ShoppingCart } from 'lucide-react';

const CheckoutPage = () => {
  const { event, totalTickets } = useCart();

  if (!event || totalTickets === 0) {
    return <Navigate to="/events" replace />;
  }

  return (
    <div className="min-h-screen bg-dark-900 pt-24 pb-12">
      <div className="max-w-3xl mx-auto section-padding">
        <div className="flex items-center gap-3 mb-8">
          <ShoppingCart className="w-6 h-6 text-kosh-400" />
          <h1 className="text-3xl font-bold text-white">Checkout</h1>
        </div>

        <div className="glass-card p-4 mb-6">
          <div className="flex items-center gap-4">
            <img
              src={event.thumbnail_image || event.banner_image}
              alt={event.title}
              className="w-20 h-20 rounded-xl object-cover"
            />
            <div>
              <h2 className="font-bold text-white">{event.title}</h2>
              <p className="text-sm text-gray-400">{totalTickets} ticket{totalTickets > 1 ? 's' : ''} selected</p>
            </div>
          </div>
        </div>

        <CheckoutFlow />
      </div>
    </div>
  );
};

export default CheckoutPage;
