/**
 * Kosh Ticketing - Shopping Cart Context
 * Manages ticket selection state during the booking flow
 */

import React, { createContext, useContext, useReducer, useCallback } from 'react';

const CartContext = createContext(null);

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within CartProvider');
  return context;
};

// Cart actions
const ADD_TICKETS = 'ADD_TICKETS';
const UPDATE_QUANTITY = 'UPDATE_QUANTITY';
const REMOVE_TICKETS = 'REMOVE_TICKETS';
const CLEAR_CART = 'CLEAR_CART';
const SET_EVENT = 'SET_EVENT';

const cartReducer = (state, action) => {
  switch (action.type) {
    case SET_EVENT:
      return {
        ...state,
        event: action.payload,
        tickets: [],
      };

    case ADD_TICKETS:
      const existingIndex = state.tickets.findIndex(
        t => t.tierId === action.payload.tierId
      );

      if (existingIndex >= 0) {
        const updatedTickets = [...state.tickets];
        updatedTickets[existingIndex] = {
          ...updatedTickets[existingIndex],
          quantity: updatedTickets[existingIndex].quantity + action.payload.quantity,
        };
        return { ...state, tickets: updatedTickets };
      }

      return {
        ...state,
        tickets: [...state.tickets, action.payload],
      };

    case UPDATE_QUANTITY:
      return {
        ...state,
        tickets: state.tickets.map(t =>
          t.tierId === action.payload.tierId
            ? { ...t, quantity: action.payload.quantity }
            : t
        ).filter(t => t.quantity > 0),
      };

    case REMOVE_TICKETS:
      return {
        ...state,
        tickets: state.tickets.filter(t => t.tierId !== action.payload),
      };

    case CLEAR_CART:
      return {
        event: null,
        tickets: [],
      };

    default:
      return state;
  }
};

export const CartProvider = ({ children }) => {
  const [state, dispatch] = useReducer(cartReducer, {
    event: null,
    tickets: [],
  });

  const setEvent = useCallback((event) => {
    dispatch({ type: SET_EVENT, payload: event });
  }, []);

  const addTickets = useCallback((tierId, tierName, price, quantity, maxPerOrder) => {
    dispatch({
      type: ADD_TICKETS,
      payload: { tierId, tierName, price, quantity, maxPerOrder },
    });
  }, []);

  const updateQuantity = useCallback((tierId, quantity) => {
    dispatch({ type: UPDATE_QUANTITY, payload: { tierId, quantity } });
  }, []);

  const removeTickets = useCallback((tierId) => {
    dispatch({ type: REMOVE_TICKETS, payload: tierId });
  }, []);

  const clearCart = useCallback(() => {
    dispatch({ type: CLEAR_CART });
  }, []);

  // Calculate totals
  const subtotal = state.tickets.reduce(
    (sum, t) => sum + t.price * t.quantity, 0
  );
  const fees = subtotal * 0.05 + 0.99;
  const total = subtotal + fees;
  const totalTickets = state.tickets.reduce((sum, t) => sum + t.quantity, 0);

  const value = {
    ...state,
    subtotal,
    fees,
    total,
    totalTickets,
    setEvent,
    addTickets,
    updateQuantity,
    removeTickets,
    clearCart,
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};
