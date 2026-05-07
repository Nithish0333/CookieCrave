import React, { useState } from 'react';
import { Container, Card, Form, Row, Col, Button, Alert } from 'react-bootstrap';

const GiftingCookiesPage = () => {
  const [submitted, setSubmitted] = useState(false);
  const [form, setForm] = useState({
    senderName: '',
    senderPhone: '',
    recipientName: '',
    recipientPhone: '',
    address: '',
    city: '',
    state: '',
    pincode: '',
    location: '',
    giftMessage: '',
    deliveryDate: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <Container>
      <div className="text-center mb-4">
        <i className="bi bi-gift display-4 text-warning"></i>
        <h1 className="mt-3 fw-bold">Gifting Cookies</h1>
        <p className="lead text-muted">Send delicious cookies as gifts to your loved ones.</p>
      </div>

      <Card className="border-0 shadow-sm">
        <Card.Body className="p-4">
          <h5 className="fw-bold mb-4">Gift Delivery Details</h5>

          {submitted && (
            <Alert variant="success" dismissible onClose={() => setSubmitted(false)}>
              Thank you! Your gift order has been received. We'll get in touch soon to confirm delivery.
            </Alert>
          )}

          <Form onSubmit={handleSubmit}>
            <h6 className="text-muted mb-3">Your details (Sender)</h6>
            <Row className="g-3 mb-4">
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Your name</Form.Label>
                  <Form.Control
                    type="text"
                    name="senderName"
                    placeholder="Enter your full name"
                    value={form.senderName}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Your phone number</Form.Label>
                  <Form.Control
                    type="tel"
                    name="senderPhone"
                    placeholder="e.g. 9876543210"
                    value={form.senderPhone}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <h6 className="text-muted mb-3">Recipient details</h6>
            <Row className="g-3 mb-4">
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Recipient name</Form.Label>
                  <Form.Control
                    type="text"
                    name="recipientName"
                    placeholder="Who should receive the gift?"
                    value={form.recipientName}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Recipient phone number</Form.Label>
                  <Form.Control
                    type="tel"
                    name="recipientPhone"
                    placeholder="e.g. 9876543210"
                    value={form.recipientPhone}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <h6 className="text-muted mb-3">Delivery address</h6>
            <Row className="g-3 mb-4">
              <Col md={12}>
                <Form.Group>
                  <Form.Label>Address</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={2}
                    name="address"
                    placeholder="House no., building, street, area"
                    value={form.address}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>City</Form.Label>
                  <Form.Control
                    type="text"
                    name="city"
                    placeholder="City"
                    value={form.city}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>State</Form.Label>
                  <Form.Control
                    type="text"
                    name="state"
                    placeholder="State"
                    value={form.state}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={4}>
                <Form.Group>
                  <Form.Label>Pincode</Form.Label>
                  <Form.Control
                    type="text"
                    name="pincode"
                    placeholder="Pincode"
                    value={form.pincode}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={12}>
                <Form.Group>
                  <Form.Label>Location / Landmark</Form.Label>
                  <Form.Control
                    type="text"
                    name="location"
                    placeholder="Nearby landmark for easy delivery"
                    value={form.location}
                    onChange={handleChange}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Row className="g-3 mb-4">
              <Col md={6}>
                <Form.Group>
                  <Form.Label>Preferred delivery date</Form.Label>
                  <Form.Control
                    type="date"
                    name="deliveryDate"
                    value={form.deliveryDate}
                    onChange={handleChange}
                  />
                </Form.Group>
              </Col>
              <Col md={12}>
                <Form.Group>
                  <Form.Label>Gift message (optional)</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={2}
                    name="giftMessage"
                    placeholder="Add a personal message for the recipient"
                    value={form.giftMessage}
                    onChange={handleChange}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Button type="submit" variant="primary" className="px-4">
              Place Gift Order
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default GiftingCookiesPage;
