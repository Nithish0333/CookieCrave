import React, { createContext, useContext, useState, useMemo } from 'react';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [items, setItems] = useState([]);

  const addToCart = (product, quantity = 1) => {
    setItems(prev => {
      const existing = prev.find(i => i.id === product.id);
      if (existing) {
        return prev.map(i =>
          i.id === product.id ? { ...i, quantity: i.quantity + quantity } : i
        );
      }
      return [...prev, { ...product, quantity }];
    });
  };

  const removeFromCart = (productId) => {
    setItems(prev => prev.filter(i => i.id !== productId));
  };

  const updateQuantity = (productId, quantity) => {
    if (quantity <= 0) {
      setItems(prev => prev.filter(i => i.id !== productId));
      return;
    }
    setItems(prev =>
      prev.map(i => (i.id === productId ? { ...i, quantity } : i))
    );
  };

  const clearCart = () => setItems([]);

  const summary = useMemo(() => {
    const itemCount = items.reduce((sum, i) => sum + i.quantity, 0);
    const total = items.reduce((sum, i) => sum + Number(i.price) * i.quantity, 0);
    return { itemCount, total };
  }, [items]);

  const value = {
    items,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    ...summary,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};

export const useCart = () => {
  const ctx = useContext(CartContext);
  if (!ctx) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return ctx;
};

