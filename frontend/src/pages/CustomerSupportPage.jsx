import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Badge, Tab, Tabs, Accordion } from 'react-bootstrap';

const CustomerSupportPage = () => {
  const [ticketId, setTicketId] = useState('');
  const [email, setEmail] = useState('');

  const handleTrackTicket = (e) => {
    e.preventDefault();
    alert(`Tracking ticket: ${ticketId} for email: ${email}`);
  };

  return (
    <Container>
      <div className="text-center mb-5">
        <h1 className="display-5 fw-bold mb-3">Customer Support Center</h1>
        <p className="lead text-muted">We're here to help! Get comprehensive support through multiple channels.</p>
        <div className="d-flex justify-content-center gap-3 flex-wrap">
          <Badge bg="success" className="px-3 py-2">
            <i className="bi bi-clock me-1"></i> Average Response: 2 hours
          </Badge>
          <Badge bg="info" className="px-3 py-2">
            <i className="bi bi-headset me-1"></i> 24/7 Emergency Support
          </Badge>
          <Badge bg="primary" className="px-3 py-2">
            <i className="bi bi-award me-1"></i> 98% Satisfaction Rate
          </Badge>
        </div>
      </div>

      <Tabs defaultActiveKey="faq" className="mb-4">
        <Tab eventKey="faq" title="FAQ">
          <Row>
            <Col md={8} className="mx-auto">
              <Card className="border-0 shadow-sm">
                <Card.Body className="p-4">
                  <h4 className="fw-bold mb-4">Frequently Asked Questions</h4>
                  <Accordion>
                    <Accordion.Item eventKey="0">
                      <Accordion.Header>How can I track my order?</Accordion.Header>
                      <Accordion.Body>
                        You can track your order by logging into your dashboard and viewing the "My Orders" section. You'll receive real-time updates via email and SMS as well.
                      </Accordion.Body>
                    </Accordion.Item>
                    <Accordion.Item eventKey="1">
                      <Accordion.Header>What is your return policy?</Accordion.Header>
                      <Accordion.Body>
                        We offer a 100% satisfaction guarantee. If you're not satisfied with your order, please contact us within 24 hours of delivery for a replacement or refund.
                      </Accordion.Body>
                    </Accordion.Item>
                    <Accordion.Item eventKey="2">
                      <Accordion.Header>Do you offer bulk discounts?</Accordion.Header>
                      <Accordion.Body>
                        Yes! We offer wholesale pricing for orders of 50+ boxes. Visit our Wholesale & Bulk Orders page for more details and to request a custom quote.
                      </Accordion.Body>
                    </Accordion.Item>
                    <Accordion.Item eventKey="3">
                      <Accordion.Header>How long does delivery take?</Accordion.Header>
                      <Accordion.Body>
                        Standard delivery takes 2-4 business days. Express delivery is available for major cities (1-2 days). International shipping takes 7-10 business days.
                      </Accordion.Body>
                    </Accordion.Item>
                    <Accordion.Item eventKey="4">
                      <Accordion.Header>What payment methods do you accept?</Accordion.Header>
                      <Accordion.Body>
                        We accept all major credit/debit cards, UPI, net banking, wallets (PayTM, PhonePe), and cash on delivery for orders below ₹2000.
                      </Accordion.Body>
                    </Accordion.Item>
                    <Accordion.Item eventKey="5">
                      <Accordion.Header>How do I report a problem with my order?</Accordion.Header>
                      <Accordion.Body>
                        Contact our support team immediately via phone, WhatsApp, or email. For urgent issues, mark them as "Emergency" priority and we'll respond within 30 minutes.
                      </Accordion.Body>
                    </Accordion.Item>
                  </Accordion>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>

        <Tab eventKey="tracking" title="Track Ticket">
          <Row>
            <Col md={6} className="mx-auto">
              <Card className="border-0 shadow-sm">
                <Card.Body className="p-4">
                  <h4 className="fw-bold mb-4">Track Your Support Ticket</h4>
                  <Form onSubmit={handleTrackTicket}>
                    <Form.Group className="mb-3">
                      <Form.Label>Ticket ID</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="Enter your ticket ID (e.g., TKT-ABC123XYZ)"
                        value={ticketId}
                        onChange={(e) => setTicketId(e.target.value)}
                        required
                      />
                    </Form.Group>
                    <Form.Group className="mb-3">
                      <Form.Label>Email Address</Form.Label>
                      <Form.Control
                        type="email"
                        placeholder="Enter your registered email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                      />
                    </Form.Group>
                    <Button type="submit" variant="primary" className="w-100">
                      <i className="bi bi-search me-2"></i> Track Ticket
                    </Button>
                  </Form>
                  <div className="mt-4 p-3 bg-light rounded">
                    <p className="mb-0 small text-muted">
                      <strong>Note:</strong> You can also check your ticket status by logging into your dashboard and visiting the "Support Tickets" section.
                    </p>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>

        <Tab eventKey="livechat" title="Live Chat">
          <Row>
            <Col md={8} className="mx-auto">
              <Card className="border-0 shadow-sm">
                <Card.Body className="p-4 text-center">
                  <h4 className="fw-bold mb-4">Live Chat Support</h4>
                  <div className="mb-4">
                    <div className="d-inline-flex align-items-center justify-content-center bg-success text-white rounded-circle mb-3" style={{ width: '80px', height: '80px' }}>
                      <i className="bi bi-chat-dots-fill" style={{ fontSize: '2rem' }}></i>
                    </div>
                    <h5>Chat with Our Support Team</h5>
                    <p className="text-muted mb-4">Get instant help from our friendly support agents</p>
                  </div>
                  
                  <div className="d-grid gap-2 mx-auto" style={{ maxWidth: '300px' }}>
                    <Button variant="success" size="lg" onClick={() => window.open('https://wa.me/919876543210')}>
                      <i className="bi bi-whatsapp me-2"></i> Start WhatsApp Chat
                    </Button>
                    <Button variant="outline-primary" onClick={() => alert('Live chat feature coming soon!')}>
                      <i className="bi bi-chat-text me-2"></i> Website Live Chat
                    </Button>
                  </div>

                  <div className="mt-4">
                    <Badge bg="success" className="me-2">Online Now</Badge>
                    <Badge bg="info">Average Wait: 2 minutes</Badge>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>

        <Tab eventKey="quickcontact" title="Quick Contact">
          <Row>
            <Col md={8} className="mx-auto">
              <Card className="border-0 shadow-sm">
                <Card.Body className="p-4">
                  <h4 className="fw-bold mb-4">Quick Contact Options</h4>
                  
                  <Row className="g-4">
                    <Col md={6}>
                      <Card className="h-100 border-0 bg-light">
                        <Card.Body className="text-center">
                          <div className="d-inline-flex align-items-center justify-content-center bg-success text-white rounded-circle mb-3" style={{ width: '60px', height: '60px' }}>
                            <i className="bi bi-telephone-fill" style={{ fontSize: '1.5rem' }}></i>
                          </div>
                          <h6 className="fw-bold">Phone Support</h6>
                          <p className="text-muted small mb-3">Call us directly for immediate assistance</p>
                          <Button variant="success" size="sm" onClick={() => window.location.href = 'tel:+919876543210'}>
                            Call Now
                          </Button>
                          <div className="mt-2">
                            <small className="text-muted">Mon-Sat: 9:00 AM - 7:00 PM</small>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                    <Col md={6}>
                      <Card className="h-100 border-0 bg-light">
                        <Card.Body className="text-center">
                          <div className="d-inline-flex align-items-center justify-content-center bg-info text-white rounded-circle mb-3" style={{ width: '60px', height: '60px' }}>
                            <i className="bi bi-whatsapp" style={{ fontSize: '1.5rem' }}></i>
                          </div>
                          <h6 className="fw-bold">WhatsApp Support</h6>
                          <p className="text-muted small mb-3">Chat with us on WhatsApp for quick responses</p>
                          <Button variant="info" size="sm" onClick={() => window.location.href = 'https://wa.me/919876543210'}>
                            Chat on WhatsApp
                          </Button>
                          <div className="mt-2">
                            <small className="text-muted">24/7 Available</small>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                    <Col md={6}>
                      <Card className="h-100 border-0 bg-light">
                        <Card.Body className="text-center">
                          <div className="d-inline-flex align-items-center justify-content-center bg-primary text-white rounded-circle mb-3" style={{ width: '60px', height: '60px' }}>
                            <i className="bi bi-envelope-fill" style={{ fontSize: '1.5rem' }}></i>
                          </div>
                          <h6 className="fw-bold">Email Support</h6>
                          <p className="text-muted small mb-3">Send us detailed queries via email</p>
                          <Button variant="primary" size="sm" onClick={() => window.open('mailto:support@cookiecrave.com')}>
                            Send Email
                          </Button>
                          <div className="mt-2">
                            <small className="text-muted">Response within 2 hours</small>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                    <Col md={6}>
                      <Card className="h-100 border-0 bg-light">
                        <Card.Body className="text-center">
                          <div className="d-inline-flex align-items-center justify-content-center bg-danger text-white rounded-circle mb-3" style={{ width: '60px', height: '60px' }}>
                            <i className="bi bi-exclamation-triangle-fill" style={{ fontSize: '1.5rem' }}></i>
                          </div>
                          <h6 className="fw-bold">Emergency Support</h6>
                          <p className="text-muted small mb-3">For urgent issues that need immediate attention</p>
                          <Button variant="danger" size="sm" onClick={() => window.location.href = 'tel:+919876543210'}>
                            Emergency Call
                          </Button>
                          <div className="mt-2">
                            <small className="text-muted">24/7 Available</small>
                          </div>
                        </Card.Body>
                      </Card>
                    </Col>
                  </Row>

                  <div className="mt-4 p-3 bg-light rounded">
                    <h6 className="fw-bold mb-2">Contact Information</h6>
                    <div className="row">
                      <div className="col-md-4">
                        <p className="mb-1 small"><strong>Email:</strong></p>
                        <p className="mb-0 small">support@cookiecrave.com</p>
                      </div>
                      <div className="col-md-4">
                        <p className="mb-1 small"><strong>Phone:</strong></p>
                        <p className="mb-0 small">+91 98765 43210</p>
                      </div>
                      <div className="col-md-4">
                        <p className="mb-1 small"><strong>Address:</strong></p>
                        <p className="mb-0 small">CookieCrave HQ, India</p>
                      </div>
                    </div>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Tab>
      </Tabs>
    </Container>
  );
};

export default CustomerSupportPage;
