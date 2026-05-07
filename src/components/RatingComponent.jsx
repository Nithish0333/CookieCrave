import React, { useState, useEffect } from 'react';
import { Card, Button, Form, Row, Col, Alert, Spinner } from 'react-bootstrap';
import api from '../api';
import analytics from '../services/analyticsService';

const RatingComponent = ({ productId, productName }) => {
  const [ratings, setRatings] = useState([]);
  const [userRating, setUserRating] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);
  const [formData, setFormData] = useState({
    rating: 5,
    review: ''
    
  });

  useEffect(() => {
    fetchRatings();
  }, [productId]);

  const fetchRatings = async () => {
    try {
      setLoading(true);
      const response = await api.get(`ratings/?product_id=${productId}`);
      setRatings(response.data);
      
      // Check if current user has already rated
      const userRate = response.data.find(r => r.user === (localStorage.getItem('userId') || null));
      setUserRating(userRate);
      
      if (userRate) {
        setFormData({
          rating: userRate.rating,
          review: userRate.review
        });
      }
      
      setError(null);
    } catch (err) {
      console.error('Error fetching ratings:', err);
      setError('Failed to load ratings');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setSubmitting(true);
      
      if (userRating) {
        // Update existing rating
        await api.patch(`ratings/${userRating.id}/`, {
          rating: parseInt(formData.rating),
          review: formData.review
        });
        setMessage('Rating updated successfully!');
      } else {
        // Create new rating
        await api.post('ratings/', {
          product: productId,
          rating: parseInt(formData.rating),
          review: formData.review
        });
        setMessage('Rating submitted successfully!');
      }

      // Track rating submission
      analytics.track('product_rated', {
        product_id: productId,
        product_name: productName,
        rating: parseInt(formData.rating),
        has_review: formData.review.length > 0
      });

      // Refetch ratings
      await fetchRatings();
      setError(null);
      
      setTimeout(() => setMessage(null), 3000);
    } catch (err) {
      console.error('Error submitting rating:', err);
      setError(err.response?.data?.detail || 'Failed to submit rating');
    } finally {
      setSubmitting(false);
    }
  };

  const averageRating = ratings.length > 0
    ? (ratings.reduce((sum, r) => sum + r.rating, 0) / ratings.length).toFixed(1)
    : 0;

  const StarIcon = ({ filled }) => (
    <span style={{ color: filled ? '#ffc107' : '#e9ecef', marginRight: '4px' }}>
      ★
    </span>
  );

  return (
    <div className="rating-section my-4">
      {/* Rating Summary */}
      <Card className="mb-4">
        <Card.Body>
          <Card.Title as="h5">Customer Ratings</Card.Title>
          <Row className="align-items-center">
            <Col md={4}>
              <div className="text-center">
                <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#ffc107' }}>
                  {averageRating}
                </div>
                <div>
                  {[1, 2, 3, 4, 5].map(i => (
                    <StarIcon key={i} filled={i <= Math.round(averageRating)} />
                  ))}
                </div>
                <small className="text-muted">
                  Based on {ratings.length} review{ratings.length !== 1 ? 's' : ''}
                </small>
              </div>
            </Col>
            <Col md={8}>
              {ratings.length === 0 ? (
                <p className="text-muted">No ratings yet. Be the first to rate!</p>
              ) : (
                <div>
                  {[5, 4, 3, 2, 1].map(star => {
                    const count = ratings.filter(r => r.rating === star).length;
                    const percentage = (count / ratings.length) * 100;
                    return (
                      <div key={star} className="mb-2">
                        <div className="d-flex align-items-center">
                          <small style={{ minWidth: '40px' }}>{star} Star{star !== 1 ? 's' : ''}</small>
                          <div
                            style={{
                              backgroundColor: '#e9ecef',
                              height: '6px',
                              flex: 1,
                              margin: '0 10px',
                              borderRadius: '3px',
                              overflow: 'hidden'
                            }}
                          >
                            <div
                              style={{
                                backgroundColor: '#ffc107',
                                height: '100%',
                                width: `${percentage}%`
                              }}
                            />
                          </div>
                          <small className="text-muted" style={{ minWidth: '40px', textAlign: 'right' }}>
                            {count}
                          </small>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Submit Rating Form */}
      <Card className="mb-4">
        <Card.Body>
          <Card.Title as="h5">
            {userRating ? 'Update Your Rating' : 'Share Your Rating'}
          </Card.Title>

          {error && <Alert variant="danger">{error}</Alert>}
          {message && <Alert variant="success">{message}</Alert>}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Rating</Form.Label>
              <div>
                {[1, 2, 3, 4, 5].map(star => (
                  <Button
                    key={star}
                    variant={formData.rating >= star ? 'warning' : 'outline-secondary'}
                    size="sm"
                    style={{
                      margin: '0 4px',
                      padding: '8px 12px',
                      fontSize: '20px'
                    }}
                    onClick={() => setFormData(prev => ({ ...prev, rating: star }))}
                    type="button"
                  >
                    ★
                  </Button>
                ))}
              </div>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label htmlFor="review">Review (Optional)</Form.Label>
              <Form.Control
                id="review"
                as="textarea"
                rows={4}
                name="review"
                value={formData.review}
                onChange={handleInputChange}
                placeholder="Share your experience with this product..."
              />
            </Form.Group>

            <Button
              variant="primary"
              type="submit"
              disabled={submitting}
              className="w-100"
            >
              {submitting ? (
                <>
                  <Spinner animation="border" size="sm" className="me-2" />
                  Submitting...
                </>
              ) : userRating ? (
                'Update Rating'
              ) : (
                'Submit Rating'
              )}
            </Button>
          </Form>
        </Card.Body>
      </Card>

      {/* Display All Ratings */}
      {ratings.length > 0 && (
        <Card>
          <Card.Body>
            <Card.Title as="h5">Reviews</Card.Title>
            {loading ? (
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            ) : (
              <div>
                {ratings.map(rating => (
                  <div key={rating.id} className="mb-3 pb-3 border-bottom">
                    <div className="d-flex justify-content-between align-items-start">
                      <div>
                        <strong>{rating.user_username}</strong>
                        <div>
                          {[1, 2, 3, 4, 5].map(i => (
                            <StarIcon key={i} filled={i <= rating.rating} />
                          ))}
                        </div>
                      </div>
                      <small className="text-muted">
                        {new Date(rating.created_at).toLocaleDateString()}
                      </small>
                    </div>
                    {rating.review && (
                      <p className="mb-0 mt-2">{rating.review}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </Card.Body>
        </Card>
      )}
    </div>
  );
};

export default RatingComponent;
