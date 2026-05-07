import React, { useState, useEffect, useRef } from 'react';
import { Container, Button, Spinner, Alert } from 'react-bootstrap';
import { ChevronLeft, ChevronRight, Star, ShoppingCart as IconShoppingCart } from 'lucide-react';
import { useCart } from '../CartContext';
import WishlistButton from './WishlistButton';
import { getProductImageUrl, getPlaceholderImageUrl } from '../utils/imageUtils';
import '../styles/RecommendationCarousel.css';

const RecommendationCarousel = ({ items, title, algorithm = 'hybrid', isLoading = false, error = null }) => {
  const [scrollPosition, setScrollPosition] = useState(0);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(true);
  const [hoveredItemId, setHoveredItemId] = useState(null);
  const carouselRef = useRef(null);
  const { addToCart } = useCart();

  const containerWidth = 300; // Width of each carousel item in pixels
  const containerMargin = 16; // Margin between items

  const handleScroll = (direction) => {
    if (!carouselRef.current) return;

    const scrollAmount = containerWidth + containerMargin;
    const container = carouselRef.current;
    let newPosition = scrollPosition;

    if (direction === 'left') {
      newPosition = Math.max(0, scrollPosition - scrollAmount);
    } else {
      const maxScroll = container.scrollWidth - container.clientWidth;
      newPosition = Math.min(maxScroll, scrollPosition + scrollAmount);
    }

    container.scrollTo({ left: newPosition, behavior: 'smooth' });
    setScrollPosition(newPosition);
  };

  const handleCarouselScroll = () => {
    if (!carouselRef.current) return;
    const { scrollLeft, scrollWidth, clientWidth } = carouselRef.current;
    setScrollPosition(scrollLeft);
    setCanScrollLeft(scrollLeft > 0);
    setCanScrollRight(scrollLeft < scrollWidth - clientWidth - 10);
  };

  useEffect(() => {
    const container = carouselRef.current;
    if (container) {
      container.addEventListener('scroll', handleCarouselScroll);
      handleCarouselScroll();
      return () => container.removeEventListener('scroll', handleCarouselScroll);
    }
  }, [items]);

  const handleAddToCart = (e, product) => {
    e.stopPropagation();
    addToCart(product, 1);
  };

  if (isLoading) {
    return (
      <section className="recommendation-carousel-section">
        <Container>
          <h2 className="carousel-title">{title}</h2>
          <div className="carousel-loading">
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading recommendations...</span>
            </Spinner>
          </div>
        </Container>
      </section>
    );
  }

  if (error) {
    return (
      <section className="recommendation-carousel-section">
        <Container>
          <h2 className="carousel-title">{title}</h2>
          <Alert variant="warning">Failed to load recommendations. Please try again.</Alert>
        </Container>
      </section>
    );
  }

  if (!items || items.length === 0) {
    return null;
  }

  return (
    <section className="recommendation-carousel-section">
      <Container fluid>
        <div className="carousel-header">
          <h2 className="carousel-title">{title}</h2>
          <span className="carousel-subtitle">
            {algorithm === 'hybrid' && '✨ Tailored for you'}
            {algorithm === 'trending' && '🔥 Trending'}
            {algorithm === 'collaborative' && '👥 Chosen by others like you'}
            {algorithm === 'content_based' && '📚 Based on your interests'}
          </span>
        </div>

        {items.length > 0 && (
          <div className="carousel-wrapper">
            {canScrollLeft && (
              <button
                className="carousel-arrow carousel-arrow-left"
                onClick={() => handleScroll('left')}
                aria-label="Scroll left"
              >
                <ChevronLeft size={28} />
              </button>
            )}

            <div
              className="carousel-container"
              ref={carouselRef}
            >
              {items.map((item) => (
                <div
                  key={item.id}
                  className="carousel-item-wrapper"
                  onMouseEnter={() => setHoveredItemId(item.id)}
                  onMouseLeave={() => setHoveredItemId(null)}
                >
                  <div className="carousel-item">
                    <div className="carousel-item-image-container">
                      <img
                        src={getProductImageUrl(item.image || item.image_url, getPlaceholderImageUrl(item.name))}
                        alt={item.name}
                        className="carousel-item-image"
                        crossOrigin="anonymous"
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = getPlaceholderImageUrl(item.name);
                        }}
                      />
                      <div className="carousel-item-overlay">
                        {hoveredItemId === item.id && (
                          <div className="carousel-item-actions">
                            <button
                              className="action-button add-to-cart-btn"
                              onClick={(e) => handleAddToCart(e, item)}
                              title="Add to cart"
                            >
                              <IconShoppingCart size={20} />
                              Add to Cart
                            </button>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="carousel-item-content">
                      <h3 className="carousel-item-name">{item.name}</h3>
                      <p className="carousel-item-category">{item.category_name}</p>

                      <div className="carousel-item-footer">
                        <div className="price-rating">
                          <span className="price">₹{item.price}</span>
                          {item.rating && (
                            <span className="rating">
                              <Star size={14} fill="#FFD700" color="#FFD700" />
                              {item.rating.toFixed(1)}
                            </span>
                          )}
                        </div>
                        <WishlistButton 
                          productId={item.id} 
                          productName={item.name}
                          className="btn-sm p-1"
                        />
                      </div>

                      {item.stock && item.stock > 0 && (
                        <div className="stock-badge in-stock">In Stock</div>
                      )}
                      {item.stock === 0 && (
                        <div className="stock-badge out-of-stock">Out of Stock</div>
                      )}
                    </div>
                  </div>
                  {item.confidence_score && (
                    <div className="recommendation-badge">
                      {Math.round(item.confidence_score * 100)}% match
                    </div>
                  )}
                </div>
              ))}
            </div>

            {canScrollRight && items.length > 4 && (
              <button
                className="carousel-arrow carousel-arrow-right"
                onClick={() => handleScroll('right')}
                aria-label="Scroll right"
              >
                <ChevronRight size={28} />
              </button>
            )}
          </div>
        )}
      </Container>
    </section>
  );
};

export default RecommendationCarousel;
