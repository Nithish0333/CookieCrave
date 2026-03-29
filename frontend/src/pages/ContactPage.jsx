import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import analytics from '../services/analyticsService';

const ContactPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [ticketId, setTicketId] = useState('');
  const [urgency, setUrgency] = useState('normal');
  const [issueType, setIssueType] = useState('general');

  useEffect(() => {
    analytics.trackContactPageView();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    const newTicketId = 'TKT-' + Math.random().toString(36).substr(2, 9).toUpperCase();
    setTicketId(newTicketId);
    setSubmitted(true);
    setName('');
    setEmail('');
    setMessage('');
  };

  return (
    <Container>
      <div className="text-center mb-5">
        <h1 className="display-5 fw-bold mb-3">Contact Us</h1>
        <p className="lead text-muted">Have a question or need help? Create a support ticket and we'll get back to you soon.</p>
      </div>

      <Row className="justify-content-center">
        <Col md={8} lg={6}>
          <Card className="border-0 shadow-sm">
            <Card.Body className="p-4">
              {submitted && (
                <Alert variant="success" dismissible onClose={() => setSubmitted(false)}>
                  <Alert.Heading>Ticket Created Successfully!</Alert.Heading>
                  <p className="mb-2">Thank you! Your support ticket has been created.</p>
                  <p className="mb-0"><strong>Ticket ID:</strong> {ticketId}</p>
                  <small className="text-muted">We'll respond within 2 hours during business hours.</small>
                </Alert>
              )}
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Issue Type</Form.Label>
                  <Form.Select value={issueType} onChange={(e) => setIssueType(e.target.value)}>
                    <option value="general">General Inquiry</option>
                    <option value="order">Order Issue</option>
                    <option value="payment">Payment Problem</option>
                    <option value="technical">Technical Support</option>
                    <option value="wholesale">Wholesale/Bulk Order</option>
                    <option value="complaint">Complaint</option>
                  </Form.Select>
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Urgency Level</Form.Label>
                  <div className="d-flex gap-2">
                    <Form.Check
                      type="radio"
                      label="Normal"
                      name="urgency"
                      value="normal"
                      checked={urgency === 'normal'}
                      onChange={(e) => setUrgency(e.target.value)}
                    />
                    <Form.Check
                      type="radio"
                      label="High"
                      name="urgency"
                      value="high"
                      checked={urgency === 'high'}
                      onChange={(e) => setUrgency(e.target.value)}
                    />
                    <Form.Check
                      type="radio"
                      label="Emergency"
                      name="urgency"
                      value="emergency"
                      checked={urgency === 'emergency'}
                      onChange={(e) => setUrgency(e.target.value)}
                    />
                  </div>
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Name</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Your name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    placeholder="your@email.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </Form.Group>
                <Form.Group className="mb-4">
                  <Form.Label>Message</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={4}
                    placeholder="Describe your issue in detail..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    required
                  />
                </Form.Group>
                <Button type="submit" variant="primary" className="w-100">
                  <i className="bi bi-send me-2"></i> Create Support Ticket
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
        <Col md={4} className="mt-4 mt-md-0">
          <Card className="border-0 shadow-sm h-100">
            <Card.Body className="p-4">
              <h6 className="fw-bold mb-3">Need More Help?</h6>
              <p className="mb-3">For comprehensive support options, visit our Customer Support Center:</p>
              <Button variant="outline-primary" size="sm" className="w-100 mb-3" onClick={() => window.location.href = '/customer-support'}>
                <i className="bi bi-headset me-2"></i> Customer Support Center
              </Button>
              
              <hr />

              <h6 className="fw-bold mb-3">Quick Contact Info</h6>
              <div className="small">
                <p className="mb-2">
                  <i className="bi bi-envelope me-2 text-muted"></i>
                  support@cookiecrave.com
                </p>
                <p className="mb-2">
                  <i className="bi bi-telephone me-2 text-muted"></i>
                  +91 98765 43210
                </p>
                <p className="mb-0">
                  <i className="bi bi-geo-alt me-2 text-muted"></i>
                  CookieCrave HQ, India
                </p>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default ContactPage;
