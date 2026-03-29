import React, { useEffect } from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import analytics from '../services/analyticsService';

const AboutPage = () => {
  useEffect(() => {
    analytics.trackAboutPageView();
  }, []);

  return (
    <Container>
      <div className="text-center mb-5">
        <img src="/logo.png" alt="CookieCrave" style={{ width: 80, marginBottom: 16 }} />
        <h1 className="display-5 fw-bold mb-3">About CookieCrave</h1>
        <p className="lead text-muted">The premium marketplace for buying and selling homemade cookies, cakes, and treats.</p>
      </div>

      <Row className="g-4 mb-5">
        <Col md={6}>
          <Card className="h-100 border-0 shadow-sm">
            <Card.Body className="p-4">
              <h5 className="fw-bold mb-3">
                <i className="bi bi-heart-fill text-danger me-2"></i>
                Our Story
              </h5>
              <p className="text-muted mb-0">
                CookieCrave was born from a love of homemade baked goods. We connect talented home bakers with cookie lovers who appreciate fresh, handcrafted treats. From chocolate chip to oatmeal, cakes to milkshakes—find your next favorite right here.
              </p>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <Card className="h-100 border-0 shadow-sm">
            <Card.Body className="p-4">
              <h5 className="fw-bold mb-3">
                <i className="bi bi-stars text-warning me-2"></i>
                What We Offer
              </h5>
              <p className="text-muted mb-0">
                Browse cookies, cakes, chocolates, milkshakes, and more. Add items to your cart, checkout securely, and enjoy delicious treats delivered or picked up. Sellers can list their creations and grow their baking business with us.
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Card className="border-0 shadow-sm bg-light">
        <Card.Body className="p-4 text-center">
          <h5 className="fw-bold mb-2">Categories</h5>
          <p className="text-muted mb-0">
            Chocolate Chip • Cakes • Milkshakes • Chocolates • Fruit and Nuts • Oatmeal
          </p>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default AboutPage;
