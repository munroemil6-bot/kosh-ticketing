/**
 * Kosh Ticketing - CheckoutFlow Component
 * 3-step checkout: Account → Attendees → Payment
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import { ordersAPI } from '../../services/api';
import { formatCurrency } from '../../utils/helpers';
import { 
  User, Ticket, CreditCard, Check, ChevronRight, 
  AlertCircle, Loader2, Lock 
} from 'lucide-react';

const CheckoutFlow = () => {
  const navigate = useNavigate();
  const { event, tickets, subtotal, fees, total, totalTickets, clearCart } = useCart();
  const { isAuthenticated, user } = useAuth();

  const [step, setStep] = useState(isAuthenticated ? 2 : 1);
  const [orderId, setOrderId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Step 1: Account/Guest Info
  const [guestEmail, setGuestEmail] = useState(user?.email || '');
  const [guestPhone, setGuestPhone] = useState(user?.phone || '');

  // Step 2: Attendees
  const [attendees, setAttendees] = useState([]);

  // Step 3: Payment
  const [paymentMethod, setPaymentMethod] = useState('card');
  const [cardNumber, setCardNumber] = useState('');
  const [cardExpiry, setCardExpiry] = useState('');
  const [cardCvc, setCardCvc] = useState('');
  const [billingName, setBillingName] = useState('');

  // Generate attendee fields based on ticket quantities
  const generateAttendeeFields = () => {
    const fields = [];
    tickets.forEach(ticket => {
      for (let i = 0; i < ticket.quantity; i++) {
        fields.push({
          tierId: ticket.tierId,
          tierName: ticket.tierName,
          first_name: '',
          last_name: '',
          email: guestEmail,
          phone: guestPhone,
        });
      }
    });
    return fields;
  };

  const handleCreateOrder = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const orderData = {
        event_id: event.id,
        tickets: tickets.map(t => ({
          ticket_tier_id: t.tierId,
          quantity: t.quantity,
        })),
        guest_email: !isAuthenticated ? guestEmail : undefined,
        guest_phone: !isAuthenticated ? guestPhone : undefined,
      };

      const response = await ordersAPI.createOrder(orderData);
      setOrderId(response.data.order.id);

      // Initialize attendee fields
      setAttendees(generateAttendeeFields());
      setStep(2);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create order');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddAttendees = async () => {
    // Validate all attendee fields
    const isValid = attendees.every(a => a.first_name && a.last_name && a.email);
    if (!isValid) {
      setError('Please fill in all attendee details');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await ordersAPI.addAttendees(orderId, { attendees });
      setStep(3);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save attendee details');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePayment = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const paymentData = {
        order_id: orderId,
        payment_method: paymentMethod,
        card_number: cardNumber,
        card_expiry: cardExpiry,
        card_cvc: cardCvc,
        billing_name: billingName,
      };

      await ordersAPI.processPayment(orderId, paymentData);
      clearCart();
      navigate(`/order-success/${orderId}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Payment failed');
    } finally {
      setIsLoading(false);
    }
  };

  const updateAttendee = (index, field, value) => {
    setAttendees(prev => prev.map((a, i) => 
      i === index ? { ...a, [field]: value } : a
    ));
  };

  const steps = [
    { num: 1, label: 'Account', icon: User },
    { num: 2, label: 'Attendees', icon: Ticket },
    { num: 3, label: 'Payment', icon: CreditCard },
  ];

  return (
    <div className="max-w-3xl mx-auto">
      {/* Progress Steps */}
      <div className="flex items-center justify-center mb-8">
        {steps.map((s, i) => (
          <React.Fragment key={s.num}>
            <div className="flex flex-col items-center">
              <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                step >= s.num
                  ? 'bg-kosh-500 text-white'
                  : 'bg-dark-700 text-gray-500'
              }`}>
                {step > s.num ? (
                  <Check className="w-5 h-5" />
                ) : (
                  <s.icon className="w-5 h-5" />
                )}
              </div>
              <span className={`text-xs mt-2 font-medium ${
                step >= s.num ? 'text-kosh-400' : 'text-gray-500'
              }`}>
                {s.label}
              </span>
            </div>
            {i < steps.length - 1 && (
              <div className={`w-16 h-0.5 mx-2 ${
                step > s.num ? 'bg-kosh-500' : 'bg-dark-700'
              }`} />
            )}
          </React.Fragment>
        ))}
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-3 text-red-400">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Order Summary Sidebar */}
      <div className="glass-card p-4 mb-6">
        <h4 className="font-semibold text-white mb-3">Order Summary</h4>
        <div className="space-y-2 text-sm">
          {tickets.map(ticket => (
            <div key={ticket.tierId} className="flex justify-between text-gray-300">
              <span>{ticket.quantity}x {ticket.tierName}</span>
              <span>{formatCurrency(ticket.price * ticket.quantity)}</span>
            </div>
          ))}
          <div className="border-t border-white/10 pt-2 flex justify-between text-gray-400">
            <span>Service Fee</span>
            <span>{formatCurrency(fees)}</span>
          </div>
          <div className="flex justify-between font-bold text-white text-base pt-1">
            <span>Total</span>
            <span className="text-kosh-400">{formatCurrency(total)}</span>
          </div>
        </div>
      </div>

      {/* Step 1: Account/Guest */}
      {step === 1 && (
        <div className="space-y-6 animate-fade-in">
          {isAuthenticated ? (
            <div className="glass-card p-6 text-center">
              <div className="w-16 h-16 bg-kosh-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Check className="w-8 h-8 text-kosh-400" />
              </div>
              <h3 className="text-lg font-bold text-white mb-1">Signed in as {user?.first_name}</h3>
              <p className="text-gray-400 text-sm">{user?.email}</p>
              <button
                onClick={handleCreateOrder}
                disabled={isLoading}
                className="btn-primary mt-6 w-full"
              >
                {isLoading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : 'Continue'}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="glass-card p-6">
                <h3 className="text-lg font-bold text-white mb-4">Guest Checkout</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm text-gray-400 mb-1.5">Email *</label>
                    <input
                      type="email"
                      value={guestEmail}
                      onChange={(e) => setGuestEmail(e.target.value)}
                      className="input-field"
                      placeholder="your@email.com"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-400 mb-1.5">Phone</label>
                    <input
                      type="tel"
                      value={guestPhone}
                      onChange={(e) => setGuestPhone(e.target.value)}
                      className="input-field"
                      placeholder="+1 (555) 000-0000"
                    />
                  </div>
                </div>
                <button
                  onClick={handleCreateOrder}
                  disabled={isLoading || !guestEmail}
                  className="btn-primary mt-6 w-full disabled:opacity-50"
                >
                  {isLoading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : 'Continue'}
                </button>
              </div>

              <div className="text-center">
                <span className="text-gray-500 text-sm">or </span>
                <button 
                  onClick={() => navigate('/login', { state: { from: '/checkout' } })}
                  className="text-kosh-400 hover:text-kosh-300 text-sm font-medium"
                >
                  Sign in for faster checkout
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Step 2: Attendee Details */}
      {step === 2 && (
        <div className="space-y-4 animate-fade-in">
          <div className="glass-card p-6">
            <h3 className="text-lg font-bold text-white mb-1">Ticket Holder Details</h3>
            <p className="text-sm text-gray-400 mb-6">
              Please provide details for each ticket holder
            </p>

            <div className="space-y-4">
              {attendees.map((attendee, index) => (
                <div key={index} className="p-4 bg-dark-700/50 rounded-xl border border-white/5">
                  <div className="flex items-center gap-2 mb-3">
                    <Ticket className="w-4 h-4 text-kosh-400" />
                    <span className="text-sm font-medium text-kosh-300">
                      {attendee.tierName} - Ticket {index + 1}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <input
                      type="text"
                      value={attendee.first_name}
                      onChange={(e) => updateAttendee(index, 'first_name', e.target.value)}
                      placeholder="First Name *"
                      className="input-field text-sm py-2.5"
                      required
                    />
                    <input
                      type="text"
                      value={attendee.last_name}
                      onChange={(e) => updateAttendee(index, 'last_name', e.target.value)}
                      placeholder="Last Name *"
                      className="input-field text-sm py-2.5"
                      required
                    />
                    <input
                      type="email"
                      value={attendee.email}
                      onChange={(e) => updateAttendee(index, 'email', e.target.value)}
                      placeholder="Email *"
                      className="input-field text-sm py-2.5 col-span-2"
                      required
                    />
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={handleAddAttendees}
              disabled={isLoading}
              className="btn-primary mt-6 w-full"
            >
              {isLoading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : 'Continue to Payment'}
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Payment */}
      {step === 3 && (
        <div className="space-y-4 animate-fade-in">
          <div className="glass-card p-6">
            <div className="flex items-center gap-2 mb-6">
              <Lock className="w-5 h-5 text-kosh-400" />
              <h3 className="text-lg font-bold text-white">Secure Payment</h3>
            </div>

            {/* Payment Method Selection */}
            <div className="grid grid-cols-3 gap-3 mb-6">
              {['card', 'paypal', 'apple'].map((method) => (
                <button
                  key={method}
                  onClick={() => setPaymentMethod(method)}
                  className={`p-3 rounded-xl border text-sm font-medium transition-all ${
                    paymentMethod === method
                      ? 'border-kosh-500 bg-kosh-500/10 text-kosh-400'
                      : 'border-white/10 text-gray-400 hover:border-white/20'
                  }`}
                >
                  {method === 'card' && 'Credit Card'}
                  {method === 'paypal' && 'PayPal'}
                  {method === 'apple' && 'Apple Pay'}
                </button>
              ))}
            </div>

            {paymentMethod === 'card' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1.5">Card Number</label>
                  <div className="relative">
                    <CreditCard className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                    <input
                      type="text"
                      value={cardNumber}
                      onChange={(e) => setCardNumber(e.target.value)}
                      placeholder="4242 4242 4242 4242"
                      className="input-field pl-12"
                      maxLength={19}
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-400 mb-1.5">Expiry</label>
                    <input
                      type="text"
                      value={cardExpiry}
                      onChange={(e) => setCardExpiry(e.target.value)}
                      placeholder="MM/YY"
                      className="input-field"
                      maxLength={5}
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-400 mb-1.5">CVC</label>
                    <input
                      type="text"
                      value={cardCvc}
                      onChange={(e) => setCardCvc(e.target.value)}
                      placeholder="123"
                      className="input-field"
                      maxLength={4}
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1.5">Name on Card</label>
                  <input
                    type="text"
                    value={billingName}
                    onChange={(e) => setBillingName(e.target.value)}
                    placeholder="John Doe"
                    className="input-field"
                  />
                </div>
              </div>
            )}

            <button
              onClick={handlePayment}
              disabled={isLoading}
              className="btn-primary mt-6 w-full text-lg py-4"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin mx-auto" />
              ) : (
                <>Pay {formatCurrency(total)}</>
              )}
            </button>

            <p className="text-center text-xs text-gray-500 mt-4">
              This is a demo payment. No real charges will be made.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default CheckoutFlow;
