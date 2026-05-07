import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Alert, Spinner, Badge } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import analytics from '../services/analyticsService';
import { useCart } from '../CartContext';
import { getProductImageUrl, getPlaceholderImageUrl } from '../utils/imageUtils';

const WishlistPage = () => {
  const [wishlist, setWishlist] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const { addToCart } = useCart();
  const navigate = useNavigate();

  useEffect(() => {
    fetchWishlist();
    analytics.trackPageView('wishlist_page');

    // Listen for wishlist updates from other components
    const handleWishlistUpdate = () => {
      console.log('Wishlist updated event received, refetching...');
      fetchWishlist();
    };

    // Refresh wishlist when page comes into focus
    const handleFocus = () => {
      console.log('Page focus detected, refreshing wishlist...');
      fetchWishlist();
    };
    
    window.addEventListener('focus', handleFocus);
    window.addEventListener('wishlistUpdated', handleWishlistUpdate);
    
    return () => {
      window.removeEventListener('focus', handleFocus);
      window.removeEventListener('wishlistUpdated', handleWishlistUpdate);
    };
  }, []);

  const fetchWishlist = async () => {
    try {
      setLoading(true);
      const response = await api.get('wishlist/');
      console.log('Wishlist response:', response.data);
      setWishlist(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching wishlist:', err);
      const errorMsg = err.response?.data?.error || err.response?.data?.detail || 'Failed to fetch wishlist';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    try {
      setRefreshing(true);
      const response = await api.get('wishlist/');
      setWishlist(response.data);
      setMessage('Wishlist updated');
      setError(null);
      setTimeout(() => setMessage(null), 2000);
    } catch (err) {
      console.error('Error refreshing wishlist:', err);
      const errorMsg = err.response?.data?.error || err.response?.data?.detail || 'Failed to refresh wishlist';
      setError(errorMsg);
    } finally {
      setRefreshing(false);
    }
  };

  const handleRemoveProduct = async (productId) => {
    try {
      setError(null);
      const response = await api.post('wishlist/remove_product/', {
        product_id: productId
      });
      
      if (response?.data) {
        setWishlist(response.data);
        setMessage('Product removed from wishlist');
        
        // Track removal
        analytics.track('product_removed_from_wishlist', {
          product_id: productId
        });

        setTimeout(() => setMessage(null), 3000);
      }
    } catch (err) {
      console.error('Error removing product:', err);
      const errorMsg = err.response?.data?.error || err.response?.data?.detail || 'Failed to remove product from wishlist';
      setError(errorMsg);
    }
  };

  const handleAddToCart = (product) => {
    try {
      // Track add to cart event
      analytics.track('add_to_cart', {
        product_id: product.id,
        product_name: product.name,
        product_price: product.price,
        product_category: product.category_name,
        source: 'wishlist_page'
      });
      
      addToCart(product, 1);
      setMessage(`${product.name} added to cart!`);
      setTimeout(() => setMessage(null), 2000);
    } catch (err) {
      console.error('Error adding to cart:', err);
      setError('Failed to add product to cart');
    }
  };

  if (loading) {
    return (
      <Container className="text-center py-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </Container>
    );
  }

  return (
    <Container className="my-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>My Wishlist</h1>
        <Button 
          variant="outline-secondary" 
          size="sm" 
          onClick={handleRefresh}
          disabled={refreshing}
        >
          {refreshing ? (
            <>
              <Spinner animation="border" size="sm" className="me-2" />
              Updating...
            </>
          ) : (
            <>
              🔄 Refresh
            </>
          )}
        </Button>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}
      {message && <Alert variant="success">{message}</Alert>}

      {!wishlist || !wishlist.products || wishlist.products.length === 0 ? (
        <Alert variant="info">
          Your wishlist is empty. Start adding products from the marketplace!
          <br />
          <Button 
            variant="link" 
            onClick={() => navigate('/home')} 
            className="mt-2"
          >
            Continue Shopping →
          </Button>
        </Alert>
      ) : (
        <>
          <div className="mb-4">
            <p className="text-muted">
              You have <strong>{wishlist.products.length}</strong> item{wishlist.products.length !== 1 ? 's' : ''} in your wishlist
            </p>
          </div>
          <Row>
            {wishlist.products && Array.isArray(wishlist.products) && wishlist.products.length > 0 ? (
              wishlist.products.map((product) => (
                <Col key={product?.id || Math.random()} md={6} lg={4} className="mb-4">
                  <Card className="h-100 shadow-sm product-card" style={{ overflow: 'hidden' }}>
                    <div style={{ height: '200px', backgroundColor: '#f8f9fa', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
                      {product?.image ? (
                        <img 
                          src={getProductImageUrl(product.image, getPlaceholderImageUrl('No Image', 300, 200))}
                          alt={product.name || 'Product'}
                          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                          crossOrigin="anonymous"
                          onError={(e) => {
                            e.target.onerror = null;
                            e.target.src = getPlaceholderImageUrl('No Image', 300, 200);
                          }}
                        />
                      ) : (
                        <span style={{ fontSize: '3rem' }}>🍪</span>
                      )}
                    </div>
                    <Card.Body className="d-flex flex-column">
                      <Card.Title>{product?.name || 'Product'}</Card.Title>
                      {product?.category_name && (
                        <Badge bg="secondary" className="mb-2" style={{ width: 'fit-content' }}>
                          {product.category_name}
                        </Badge>
                      )}
                      <Card.Text className="text-muted small" style={{ flex: 1 }}>
                        {product?.description?.substring(0, 100) || 'No description'}...
                      </Card.Text>
                      <div className="mt-3">
                        <div className="d-flex justify-content-between align-items-center mb-3">
                          <span className="h5 mb-0 text-danger fw-bold">₹{product?.price || '0'}</span>
                          <span className="text-muted small">
                            {product?.stock > 0 ? (
                              <Badge bg="success">In Stock ({product.stock})</Badge>
                            ) : (
                              <Badge bg="danger">Out of Stock</Badge>
                            )}
                          </span>
                        </div>
                        <div className="d-grid gap-2">
                          <Button 
                            variant="primary" 
                            size="sm"
                            onClick={() => handleAddToCart(product)}
                            disabled={product?.stock === 0}
                          >
                            Add to Cart
                          </Button>
                          <Button
                            variant="outline-danger"
                            size="sm"
                            onClick={() => handleRemoveProduct(product?.id)}
                          >
                            ❤️ Remove from Wishlist
                          </Button>
                        </div>
                      </div>
                    </Card.Body>
                  </Card>
                </Col>
              ))
            ) : (
              <Col>
                <Alert variant="warning">No products found in wishlist</Alert>
              </Col>
            )}
          </Row>
        </>
      )}
    </Container>
  );
};

export default WishlistPage;
