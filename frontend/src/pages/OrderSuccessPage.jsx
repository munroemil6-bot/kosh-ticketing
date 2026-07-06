import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { CheckCircle, Ticket } from 'lucide-react';

const OrderSuccessPage = () => {
  const { orderId } = useParams();

  return (
    <div className="min-h-screen bg-dark-900 flex items-center justify-center pt-16">
      <div className="max-w-md w-full section-padding text-center">
        <div className="w-20 h-20 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle className="w-10 h-10 text-emerald-400" />
        </div>

        <h1 className="text-3xl font-bold text-white mb-3">Order Confirmed!</h1>
        <p className="text-gray-400 mb-2">
          Your tickets have been booked successfully.
        </p>
        <p className="text-sm text-kosh-400 font-mono mb-8">
          Order #{orderId}
        </p>

        <div className="space-y-3">
          <Link to="/my-tickets" className="btn-primary w-full flex items-center justify-center gap-2">
            <Ticket className="w-5 h-5" />
            View My Tickets
          </Link>
          <Link to="/events" className="btn-secondary w-full flex items-center justify-center gap-2">
            Browse More Events
          </Link>
        </div>

        <div className="mt-8 p-4 bg-white/5 rounded-xl">
          <p className="text-sm text-gray-400">
            A confirmation email has been sent with your tickets attached.
          </p>
        </div>
      </div>
    </div>
  );
};

export default OrderSuccessPage;
