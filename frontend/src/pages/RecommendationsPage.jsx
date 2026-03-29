import React, { useState, useEffect } from 'react';
import { Container, Tabs, Tab, Badge, Button, Form, Row, Col, Card, Spinner } from 'react-bootstrap';
import { RefreshCw, Settings } from 'lucide-react';
import api, { recommendationAPI } from '../api';
import RecommendationCarousel from '../components/RecommendationCarousel';
import analytics from '../services/analyticsService';
import { getProductImageUrl, getPlaceholderImageUrl } from '../utils/imageUtils';
import '../styles/RecommendationsPage.css';

const RecommendationsPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [recommendationsByAlgorithm, setRecommendationsByAlgorithm] = useState({
    hybrid: [],
    trending: [],
    collaborative: [],
    content_based: [],
  });
  const [loading, setLoading] = useState({
    hybrid: false,
    trending: false,
    collaborative: false,
    content_based: false,
  });
  const [errors, setErrors] = useState({
    hybrid: null,
    trending: null,
    collaborative: null,
    content_based: null,
  });
  const [categories, setCategories] = useState([]);
  const [filters, setFilters] = useState({
    selectedCategories: [],
    priceRange: { min: null, max: null },
  });
  const [userPreferences, setUserPreferences] = useState(null);
  const [showPreferences, setShowPreferences] = useState(false);
  const [activeTab, setActiveTab] = useState('hybrid');

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('access') || sessionStorage.getItem('access');
    setIsAuthenticated(!!token);
    
    analytics.trackPageView('recommendations');
    fetchCategories();
    fetchAllRecommendations();
    fetchUserPreferences();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await api.get('categories/');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchUserPreferences = async () => {
    try {
      const response = await recommendationAPI.getUserPreferences();
      setUserPreferences(response.data);
    } catch (error) {
      console.error('Error fetching user preferences:', error);
    }
  };

  const fetchAllRecommendations = async () => {
    const algorithms = ['hybrid', 'trending', 'collaborative', 'content_based'];

    for (const algorithm of algorithms) {
      await fetchRecommendations(algorithm);
    }
  };

  const fetchRecommendations = async (algorithm) => {
    setLoading((prev) => ({ ...prev, [algorithm]: true }));
    setErrors((prev) => ({ ...prev, [algorithm]: null }));

    // Check if user is authenticated
    const token = localStorage.getItem('access') || sessionStorage.getItem('access');
    console.log(`Fetching ${algorithm} recommendations, token exists:`, !!token);

    try {
      const response = await recommendationAPI.getRecommendations(
        algorithm,
        12,
        filters.selectedCategories.length > 0 ? filters.selectedCategories : null,
        filters.priceRange.min || filters.priceRange.max ? filters.priceRange : null
      );

      console.log(`Success fetching ${algorithm} recommendations:`, response.data);
      setRecommendationsByAlgorithm((prev) => ({
        ...prev,
        [algorithm]: response.data.recommendations || [],
      }));

      analytics.track('recommendations_viewed', {
        algorithm,
        quantity: response.data.recommendations?.length || 0,
      });
    } catch (error) {
      console.error(`Error fetching ${algorithm} recommendations:`, error);
      console.error('Error response:', error.response);
      console.error('Error status:', error.response?.status);
      console.error('Error data:', error.response?.data);
      
      // Always show mock data as fallback
      setRecommendationsByAlgorithm((prev) => ({
        ...prev,
        [algorithm]: getMockRecommendations(algorithm),
      }));
      
      // Handle different error types
      if (error.response?.data?.error) {
        errorMessage = `Error: ${error.response.data.error}`;
      } else if (error.response?.data?.detail) {
        errorMessage = `Error: ${error.response.data.detail}`;
      } else if (error.response?.status === 401) {
        errorMessage = 'Please log in to see recommendations.';
      } else if (error.response?.status === 403) {
        errorMessage = 'You do not have permission to view recommendations.';
      } else if (error.response?.status === 404) {
        errorMessage = 'Recommendations service not available.';
      } else if (error.response?.status === 500) {
        errorMessage = 'Server error (500). Please try again later.';
      } else if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
        errorMessage = 'Cannot connect to the server. Please check your connection.';
      } else if (error.message) {
        errorMessage = `Error: ${error.message}`;
      }
      
      setErrors((prev) => ({
        ...prev,
        [algorithm]: errorMessage,
      }));
    } finally {
      setLoading((prev) => ({ ...prev, [algorithm]: false }));
    }
  };

  // Mock data for demo purposes
  const getMockRecommendations = (algorithm) => {
    const mockData = [
      {
        id: 1,
        name: "Classic Chocolate Chip",
        price: 299,
        stock: 15,
        image: "https://placehold.co/400x300/8B4513/FFFFFF?text=Chocolate+Chip",
        image_url: "https://placehold.co/400x300/8B4513/FFFFFF?text=Chocolate+Chip",
        category_name: "Chocolate",
        confidence_score: algorithm === 'hybrid' ? 0.95 : algorithm === 'trending' ? 0.88 : 0.92
      },
      {
        id: 2,
        name: "Vanilla Dream Cookies",
        price: 249,
        stock: 8,
        image: "https://placehold.co/400x300/FFE4B5/333333?text=Vanilla+Dream",
        image_url: "https://placehold.co/400x300/FFE4B5/333333?text=Vanilla+Dream",
        category_name: "Vanilla",
        confidence_score: algorithm === 'hybrid' ? 0.87 : algorithm === 'trending' ? 0.91 : 0.85
      },
      {
        id: 3,
        name: "Oatmeal Raisin Delight",
        price: 279,
        stock: 12,
        image: "https://placehold.co/400x300/D2691E/FFFFFF?text=Oatmeal+Raisin",
        image_url: "https://placehold.co/400x300/D2691E/FFFFFF?text=Oatmeal+Raisin",
        category_name: "Oatmeal",
        confidence_score: algorithm === 'hybrid' ? 0.82 : algorithm === 'trending' ? 0.79 : 0.88
      },
      {
        id: 4,
        name: "Double Chocolate Fudge",
        price: 329,
        stock: 6,
        image: "https://placehold.co/400x300/654321/FFFFFF?text=Double+Fudge",
        image_url: "https://placehold.co/400x300/654321/FFFFFF?text=Double+Fudge",
        category_name: "Chocolate",
        confidence_score: algorithm === 'hybrid' ? 0.90 : algorithm === 'trending' ? 0.85 : 0.87
      }
    ];
    
    return mockData;
  };

  const handleRefresh = () => {
    analytics.track('recommendations_refreshed');
    fetchAllRecommendations();
  };

  const handleFilterChange = (e) => {
    const { name, value, checked } = e.target;

    if (name === 'category') {
      setFilters((prev) => {
        const selectedCategories = checked
          ? [...prev.selectedCategories, parseInt(value)]
          : prev.selectedCategories.filter((id) => id !== parseInt(value));

        return { ...prev, selectedCategories };
      });
    } else if (name === 'minPrice') {
      setFilters((prev) => ({
        ...prev,
        priceRange: { ...prev.priceRange, min: value ? parseInt(value) : null },
      }));
    } else if (name === 'maxPrice') {
      setFilters((prev) => ({
        ...prev,
        priceRange: { ...prev.priceRange, max: value ? parseInt(value) : null },
      }));
    }
  };

  const handleApplyFilters = () => {
    fetchAllRecommendations();
  };

  const handleClearFilters = () => {
    setFilters({
      selectedCategories: [],
      priceRange: { min: null, max: null },
    });
    fetchAllRecommendations();
  };

  const algorithmTitles = {
    hybrid: '✨ Recommended For You',
    trending: '🔥 Trending This Month',
    collaborative: '👥 Users Like You Also Liked',
    content_based: '📚 Based On Your Interests',
  };

  const algorithmDescriptions = {
    hybrid: 'A blend of your preferences and current trends',
    trending: 'The most popular items right now',
    collaborative: 'Recommendations based on similar users',
    content_based: 'Items similar to what you liked before',
  };

  return (
    <Container className="recommendations-page">
      {!isAuthenticated ? (
        <div className="text-center py-5">
          <h3>Please Log In to See Recommendations</h3>
          <p className="text-muted mb-4">
            You need to be logged in to view personalized recommendations based on your preferences and browsing history.
          </p>
          <Button as="a" href="/login" variant="primary" size="lg">
            Log In to Continue
          </Button>
        </div>
      ) : (
        <>
          <div className="recommendations-header">
            <div className="header-content">
              <h1>Discover Recommendations</h1>
              <p className="header-subtitle">Personalized picks based on your taste</p>
            </div>
            <div className="header-actions">
              <Button
                variant="outline-primary"
                size="sm"
                onClick={handleRefresh}
                className="refresh-button"
                disabled={Object.values(loading).some((l) => l)}
              >
                <RefreshCw size={16} />
                {Object.values(loading).some((l) => l) ? 'Loading...' : 'Refresh'}
              </Button>
              <Button
                variant="outline-secondary"
                size="sm"
                onClick={() => setShowPreferences(!showPreferences)}
                className="preferences-button"
              >
                <Settings size={16} />
                Filters
              </Button>
            </div>
          </div>

          {showPreferences && (
            <div className="filters-panel">
              <Card>
                <Card.Body>
                  <h5 className="mb-3">Filter Recommendations</h5>

                  <div className="filter-group">
                    <label className="filter-label">Categories</label>
                    <div className="category-checkboxes">
                      {categories.map((category) => (
                        <Form.Check
                          key={category.id}
                          type="checkbox"
                          label={category.name}
                          name="category"
                          value={category.id}
                          checked={filters.selectedCategories.includes(category.id)}
                          onChange={handleFilterChange}
                          className="filter-checkbox"
                        />
                      ))}
                    </div>
                  </div>

                  <div className="filter-group">
                    <label className="filter-label">Price Range</label>
                    <Row>
                      <Col xs={6}>
                        <Form.Control
                          type="number"
                          placeholder="Min Price"
                          name="minPrice"
                          value={filters.priceRange.min || ''}
                          onChange={handleFilterChange}
                          min="0"
                        />
                      </Col>
                      <Col xs={6}>
                        <Form.Control
                          type="number"
                          placeholder="Max Price"
                          name="maxPrice"
                          value={filters.priceRange.max || ''}
                          onChange={handleFilterChange}
                          min="0"
                        />
                      </Col>
                    </Row>
                  </div>

                  <div className="filter-actions">
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={handleApplyFilters}
                      disabled={Object.values(loading).some((l) => l)}
                    >
                      Apply Filters
                    </Button>
                    <Button
                      variant="outline-secondary"
                      size="sm"
                      onClick={handleClearFilters}
                      disabled={
                        filters.selectedCategories.length === 0 &&
                        !filters.priceRange.min &&
                        !filters.priceRange.max
                      }
                    >
                      Clear All
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            </div>
          )}

          <Tabs
            activeKey={activeTab}
            onSelect={(k) => {
              setActiveTab(k);
              analytics.track('recommendation_tab_changed', { algorithm: k });
            }}
            className="recommendation-tabs mb-4"
          >
            {['hybrid', 'trending', 'collaborative', 'content_based'].map((algorithm) => (
              <Tab
                key={algorithm}
                eventKey={algorithm}
                title={
                  <span>
                    {algorithmTitles[algorithm].split(' ')[0]}{' '}
                    {algorithmTitles[algorithm].split(' ').slice(1).join(' ')}
                  </span>
                }
              >
                <div className="tab-description">
                  <p>{algorithmDescriptions[algorithm]}</p>
                </div>

                {loading[algorithm] && (
                  <div className="loading-container">
                    <Spinner animation="border" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </Spinner>
                  </div>
                )}

                {!loading[algorithm] && errors[algorithm] && (
                  <div className="alert alert-warning">{errors[algorithm]}</div>
                )}

                {!loading[algorithm] && recommendationsByAlgorithm[algorithm].length === 0 && !errors[algorithm] && (
                  <div className="no-recommendations">
                    <p>No recommendations available for this algorithm.</p>
                  </div>
                )}

                {!loading[algorithm] && recommendationsByAlgorithm[algorithm].length > 0 && (
                  <div className="recommendations-grid">
                    {recommendationsByAlgorithm[algorithm].map((item) => (
                      <div key={item.id} className="recommendation-card">
                        <div className="card-image">
                          <div style={{ height: '200px', backgroundColor: '#f8f9fa', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
                            {(item.image || item.image_url) ? (
                              <img 
                                src={getProductImageUrl(item.image || item.image_url, getPlaceholderImageUrl(item.name))}
                                alt={item.name}
                                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                                crossOrigin="anonymous"
                                onError={(e) => {
                                  e.target.onerror = null;
                                  e.target.src = getPlaceholderImageUrl(item.name);
                                }}
                              />
                            ) : (
                              <span className="cookie-icon" style={{ fontSize: '4rem' }}>🍪</span>
                            )}
                          </div>
                          {item.confidence_score && (
                            <Badge className="match-badge">
                              {Math.round(item.confidence_score * 100)}% match
                            </Badge>
                          )}
                        </div>
                        <div className="card-content">
                          <h6>{item.name}</h6>
                          <p className="card-category">{item.category_name}</p>
                          <p className="card-price">₹{item.price}</p>
                          <p className="card-stock">
                            {item.stock > 0 ? 'In Stock' : 'Out of Stock'}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </Tab>
            ))}
          </Tabs>
        </>
      )}
    </Container>
  );
};

export default RecommendationsPage;
