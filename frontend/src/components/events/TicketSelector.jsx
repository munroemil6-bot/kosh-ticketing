/**
 * Kosh Ticketing - TicketSelector Component
 * Interactive ticket tier selection with quantity controls
 */

import React, { useState } from 'react';
import { Minus, Plus, Check, Star, AlertTriangle } from 'lucide-react';
import { formatCurrency } from '../../utils/helpers';
import { useCart } from '../../context/CartContext';

const TicketSelector = ({ event, onContinue }) => {
  const { tickets, updateQuantity, subtotal, fees, total, totalTickets } = useCart();
  const [selectedTiers, setSelectedTiers] = useState({});

  const handleQuantityChange = (tier, change) => {
    const currentQty = selectedTiers[tier.id] || 0;
    const newQty = Math.max(0, Math.min(currentQty + change, tier.max_per_order, tier.tickets_available));

    setSelectedTiers(prev => ({ ...prev, [tier.id]: newQty }));
    updateQuantity(tier.id, newQty);
  };

  const getTierQuantity = (tierId) => selectedTiers[tierId] || 0;

  const isSoldOut = (tier) => tier.is_sold_out || tier.tickets_available === 0;
  const isLowStock = (tier) => !isSoldOut(tier) && tier.tickets_available <= 10;

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-bold text-white mb-4">Select Your Tickets</h3>

      {event.ticket_tiers?.map((tier) => {
        const qty = getTierQuantity(tier.id);
        const soldOut = isSoldOut(tier);
        const lowStock = isLowStock(tier);

        return (
          <div
            key={tier.id}
            className={`relative glass-card p-4 transition-all ${
              qty > 0 ? 'border-kosh-500/40 bg-kosh-500/5' : 'border-white/5'
            } ${soldOut ? 'opacity-50' : ''}`}
          >
            {/* Sold Out Overlay */}
            {soldOut && (
              <div className="absolute inset-0 bg-dark-900/60 backdrop-blur-sm rounded-2xl flex items-center justify-center z-10">
                <span className="px-4 py-2 bg-red-500/20 border border-red-500/30 rounded-xl text-red-400 font-bold">
                  Sold Out
                </span>
              </div>
            )}

            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-bold text-white">{tier.name}</h4>
                  {tier.benefits?.length > 0 && (
                    <Star className="w-4 h-4 text-kosh-400 fill-kosh-400" />
                  )}
                </div>

                {tier.description && (
                  <p className="text-sm text-gray-400 mb-2">{tier.description}</p>
                )}

                {/* Benefits */}
                {tier.benefits?.length > 0 && (
                  <ul className="space-y-1 mb-3">
                    {tier.benefits.map((benefit, idx) => (
                      <li key={idx} className="flex items-center gap-1.5 text-xs text-gray-300">
                        <Check className="w-3 h-3 text-kosh-400" />
                        {benefit}
                      </li>
                    ))}
                  </ul>
                )}

                {/* Stock indicator */}
                {lowStock && !soldOut && (
                  <div className="flex items-center gap-1.5 text-xs text-amber-400">
                    <AlertTriangle className="w-3 h-3" />
                    Only {tier.tickets_available} left
                  </div>
                )}

                {tier.percent_sold > 75 && !soldOut && !lowStock && (
                  <div className="text-xs text-gray-500">
                    {Math.round(tier.percent_sold)}% sold
                  </div>
                )}
              </div>

              <div className="text-right ml-4">
                <div className="flex items-baseline gap-1.5">
                  {tier.original_price && tier.original_price > tier.price && (
                    <span className="text-sm text-gray-500 line-through">
                      {formatCurrency(tier.original_price)}
                    </span>
                  )}
                  <span className="text-xl font-bold text-white">
                    {formatCurrency(tier.price)}
                  </span>
                </div>

                {/* Quantity Controls */}
                {!soldOut && (
                  <div className="flex items-center gap-2 mt-3">
                    <button
                      onClick={() => handleQuantityChange(tier, -1)}
                      disabled={qty === 0}
                      className="w-8 h-8 flex items-center justify-center rounded-lg bg-white/5 hover:bg-white/10 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="w-8 text-center font-semibold text-white">{qty}</span>
                    <button
                      onClick={() => handleQuantityChange(tier, 1)}
                      disabled={qty >= tier.max_per_order || qty >= tier.tickets_available}
                      className="w-8 h-8 flex items-center justify-center rounded-lg bg-kosh-500/20 hover:bg-kosh-500/30 text-kosh-400 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}

      {/* Order Summary */}
      {totalTickets > 0 && (
        <div className="glass-card p-4 space-y-2 animate-fade-in">
          <div className="flex justify-between text-sm text-gray-400">
            <span>Subtotal ({totalTickets} tickets)</span>
            <span>{formatCurrency(subtotal)}</span>
          </div>
          <div className="flex justify-between text-sm text-gray-400">
            <span>Service Fee</span>
            <span>{formatCurrency(fees)}</span>
          </div>
          <div className="border-t border-white/10 pt-2 flex justify-between">
            <span className="font-bold text-white">Total</span>
            <span className="font-bold text-xl text-kosh-400">{formatCurrency(total)}</span>
          </div>

          <button
            onClick={onContinue}
            className="w-full btn-primary mt-3"
          >
            Continue to Checkout
          </button>
        </div>
      )}
    </div>
  );
};

export default TicketSelector;
