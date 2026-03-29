import React, { useState, useEffect } from 'react';
import { Button, Toast } from 'react-bootstrap';
import api from '../api';
import analytics from '../services/analyticsService';

const WishlistButton = ({ productId, productName, className = '', onWishlistChange }) => {
  const [isInWishlist, setIsInWishlist] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState('success');

  useEffect(() => {
    checkWishlistStatus();
  }, [productId]);

  const checkWishlistStatus = async () => {
    try {
      const response = await api.get('wishlist/');
      if (response?.data?.products && Array.isArray(response.data.products)) {
        const productIds = response.data.products.map(p => p.id);
        const inWishlist = productIds.includes(parseInt(productId));
        setIsInWishlist(inWishlist);
      }
    } catch (err) {
      console.error('Error checking wishlist status:', err);
    }
  };

  const showNotification = (message, type = 'success') => {
    setToastMessage(message);
    setToastType(type);
    setShowToast(true);
    setTimeout(() => setShowToast(false), 2500);
  };

  const notifyChange = () => {
    // Notify callback if provided
    if (onWishlistChange) {
      onWishlistChange();
    }
    
    // Dispatch custom event for other components to listen
    const event = new CustomEvent('wishlistUpdated');
    window.dispatchEvent(event);
  };

  const handleWishlistToggle = async () => {
    setLoading(true);
    
    try {
      if (isInWishlist) {
        // Remove from wishlist
        const response = await api.post('wishlist/remove_product/', {
          product_id: parseInt(productId)
        });
        
        if (response?.status === 200) {
          setIsInWishlist(false);
          showNotification('Removed from wishlist', 'success');
          
          // Track removal
          analytics.track('product_removed_from_wishlist', {
            product_id: productId,
            product_name: productName
          });
          
          // Notify change
          notifyChange();
        }
      } else {
        // Add to wishlist
        const response = await api.post('wishlist/add_product/', {
          product_id: parseInt(productId)
        });
        
        if (response?.status === 200) {
          setIsInWishlist(true);
          showNotification('Added to wishlist', 'success');
          
          // Track addition
          analytics.track('product_added_to_wishlist', {
            product_id: productId,
            product_name: productName
          });
          
          // Notify change
          notifyChange();
        }
      }
    } catch (err) {
      console.error('Error toggling wishlist:', err);
      console.log('Error response:', err.response);
      
      const errorMsg = err.response?.data?.error || 
                      err.response?.data?.detail || 
                      err.message || 
                      'Error updating wishlist';
      
      showNotification(errorMsg, 'error');
      
      // Re-check status on error
      setTimeout(() => {
        checkWishlistStatus();
      }, 500);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Button
        variant={isInWishlist ? 'danger' : 'outline-danger'}
        size="sm"
        onClick={handleWishlistToggle}
        disabled={loading}
        className={`wishlist-heart-btn ${className}`}
        style={{
          borderRadius: '50%',
          width: '36px',
          height: '36px',
          padding: '0',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          border: isInWishlist ? 'none' : '2px solid #dc3545',
          backgroundColor: isInWishlist ? '#dc3545' : 'transparent',
          transition: 'all 0.2s ease'
        }}
        title={isInWishlist ? 'Remove from wishlist' : 'Add to wishlist'}
      >
        <span style={{ 
          fontSize: '16px', 
          lineHeight: '1',
          filter: isInWishlist ? 'none' : 'sepia(1) saturate(5) hue-rotate(-50deg)'
        }}>
          {isInWishlist ? '❤️' : '🤍'}
        </span>
      </Button>

      <Toast
        show={showToast}
        onClose={() => setShowToast(false)}
        delay={2500}
        autohide
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 1050
        }}
      >
        <Toast.Body 
          style={{
            backgroundColor: toastType === 'error' ? '#f8d7da' : '#d4edda',
            color: toastType === 'error' ? '#721c24' : '#155724',
            borderRadius: '8px'
          }}
        >
          {toastMessage}
        </Toast.Body>
      </Toast>
    </>
  );
};

export default WishlistButton;
