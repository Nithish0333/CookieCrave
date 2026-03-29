import { useEffect, useCallback } from 'react';

/**
 * Custom hook to sync wishlist changes across components
 * When wishlist is updated in one place, other components get notified
 */
const useWishlistSync = (callback) => {
  // Trigger the callback whenever wishlist is updated
  const notifyWishlistChange = useCallback(() => {
    if (callback) {
      callback();
    }
    
    // Dispatch custom event that other components can listen to
    const event = new CustomEvent('wishlistUpdated');
    window.dispatchEvent(event);
  }, [callback]);

  // Listen for wishlist updates
  useEffect(() => {
    const handleWishlistUpdate = () => {
      if (callback) {
        callback();
      }
    };

    window.addEventListener('wishlistUpdated', handleWishlistUpdate);
    return () => {
      window.removeEventListener('wishlistUpdated', handleWishlistUpdate);
    };
  }, [callback]);

  return { notifyWishlistChange };
};

export default useWishlistSync;
