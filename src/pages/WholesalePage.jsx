import React, { useState } from 'react';
import { Container, Row, Col, Card, Table, Button, Form, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import analytics from '../services/analyticsService';

const WholesalePage = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    company: '',
    contact_name: '',
    email: '',
    phone: '',
    quantity: '',
    event_type: '',
    delivery_date: '',
    delivery_address: '',
    budget: '',
    notes: '',
  });
  const [paymentMethod, setPaymentMethod] = useState('enquiry_only');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const loadRazorpayScript = () => {
    return new Promise((resolve) => {
      if (window.Razorpay) {
        resolve(true);
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setMessage(null);

    if (!form.contact_name || !form.email || !form.phone || !form.quantity || !form.delivery_address) {
      setError('Please fill in all required fields marked with *');
      return;
    }

    setLoading(true);

    try {
      analytics.track('wholesale_enquiry_submitted', {
        company: form.company,
        quantity: form.quantity,
        event_type: form.event_type,
        payment_method: paymentMethod,
      });

      if (paymentMethod === 'online_advance') {
        const amount = Number(form.budget) || 0;
        if (!amount || amount <= 0) {
          setError('Please enter an approximate budget amount for advance payment.');
          setLoading(false);
          return;
        }

        const razorpayLoaded = await loadRazorpayScript();
        if (!razorpayLoaded) {
          setError('Failed to load payment gateway. Please check your connection and try again.');
          setLoading(false);
          return;
        }

        // Create Razorpay order using existing payments API
        const orderData = await api.post('razorpay/create-order/', { amount }).then((res) => res.data);

        const options = {
          key: orderData.key_id,
          amount: orderData.amount * 100,
          currency: 'INR',
          name: 'CookieCrave Wholesale',
          description: 'Wholesale / bulk order advance',
          order_id: orderData.razorpay_order_id,
          prefill: {
            name: form.contact_name,
            email: form.email,
            contact: form.phone,
          },
          notes: {
            company: form.company,
            quantity: form.quantity,
            event_type: form.event_type,
          },
          handler: async function (response) {
            try {
              // Verify wholesale payment and trigger email
              await api.post('razorpay/verify-wholesale/', {
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
                email: form.email,
                contact_name: form.contact_name,
                company: form.company,
                amount: amount,
                quantity: form.quantity
              });

              analytics.track('wholesale_advance_paid', {
                amount,
                quantity: form.quantity,
              });
              setMessage(
                'Thank you! Your wholesale enquiry and advance payment have been received. A confirmation email has been sent to you. Redirecting to your dashboard...'
              );
              setLoading(false);
              setTimeout(() => {
                navigate('/dashboard');
              }, 2500);
            } catch (verifErr) {
               setError('Payment verified by bank, but we had trouble sending a confirmation email. Your enquiry has been recorded.');
               setLoading(false);
            }
          },
          modal: {
            ondismiss: function () {
              analytics.track('wholesale_advance_cancelled', {
                amount,
                quantity: form.quantity,
              });
              setError('Payment was cancelled. Your enquiry was not completed.');
              setLoading(false);
            },
          },
        };

        const rzp = new window.Razorpay(options);
        rzp.open();
      } else {
        // Enquiry only (no online payment)
        setMessage(
          'Thank you! Your wholesale enquiry has been recorded. Our team will contact you on the provided details.'
        );
        setLoading(false);
      }
    } catch (err) {
      const detail = err.message || 'Error submitting wholesale enquiry. Please try again.';
      analytics.track('wholesale_enquiry_failed', {
        error_message: detail,
      });
      setError(detail);
      setLoading(false);
    }
  };

  return (
    <Container>
      <h2 className="mb-4 fw-bold">Wholesale & Bulk Orders</h2>

      {message && <Alert variant="success">{message}</Alert>}
      {error && <Alert variant="danger">{error}</Alert>}

      <Row className="mb-4">
        <Col md={7}>
          <Card className="mb-3 shadow-sm">
            <Card.Body>
              <Card.Title className="fw-bold">Partner with CookieCrave</Card.Title>
              <Card.Text>
                Order cookies in bulk for cafés, offices, events, gift hampers, and resellers.
                Share your requirements below and optionally pay an advance online to lock in your slot.
              </Card.Text>
              <ul className="mb-0">
                <li>
                  Minimum wholesale quantity: <strong>50 boxes</strong>
                </li>
                <li>Custom packaging and branding available on request</li>
                <li>Pan-India delivery with temperature‑controlled packing options</li>
              </ul>
            </Card.Body>
          </Card>

          <Card className="shadow-sm">
            <Card.Body>
              <Card.Title className="fw-bold">How bulk ordering works</Card.Title>
              <ol className="mb-0">
                <li>Fill in the bulk enquiry form with your details.</li>
                <li>Optionally pay an advance online to confirm your slot.</li>
                <li>We send you a final quote and confirm flavours & packaging.</li>
                <li>Once confirmed, we bake fresh cookies and ship on your schedule.</li>
              </ol>
            </Card.Body>
          </Card>
        </Col>

        <Col md={5}>
          <Card className="shadow-sm">
            <Card.Body>
              <Card.Title className="fw-bold mb-3">Bulk order enquiry</Card.Title>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-2">
                  <Form.Label>Company / Organization</Form.Label>
                  <Form.Control
                    type="text"
                    name="company"
                    value={form.company}
                    onChange={handleChange}
                    placeholder="Optional"
                  />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Label>
                    Contact name <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control
                    type="text"
                    name="contact_name"
                    value={form.contact_name}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Label>
                    Email <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control type="email" name="email" value={form.email} onChange={handleChange} required />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Label>
                    Phone number <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control type="tel" name="phone" value={form.phone} onChange={handleChange} required />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Label>
                    Approx. quantity (boxes) <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control
                    type="number"
                    name="quantity"
                    value={form.quantity}
                    onChange={handleChange}
                    min="50"
                    required
                  />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Label>Event type</Form.Label>
                  <Form.Control
                    type="text"
                    name="event_type"
                    value={form.event_type}
                    onChange={handleChange}
                    placeholder="e.g. Corporate gifting, wedding, festival hampers"
                  />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Label>Preferred delivery date</Form.Label>
                  <Form.Control
                    type="date"
                    name="delivery_date"
                    value={form.delivery_date}
                    onChange={handleChange}
                  />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Label>
                    Delivery address <span className="text-danger">*</span>
                  </Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={2}
                    name="delivery_address"
                    value={form.delivery_address}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Label>Approx. budget (₹)</Form.Label>
                  <Form.Control
                    type="number"
                    name="budget"
                    value={form.budget}
                    onChange={handleChange}
                    min="0"
                    placeholder="Optional, required only for online advance"
                  />
                </Form.Group>
                <Form.Group className="mb-2">
                  <Form.Label>Additional notes</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={2}
                    name="notes"
                    value={form.notes}
                    onChange={handleChange}
                    placeholder="Flavour preferences, packaging, branding, delivery instructions..."
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Enquiry & payment option</Form.Label>
                  <div>
                    <Form.Check
                      type="radio"
                      id="wholesale-enquiry-only"
                      name="wholesale-payment-method"
                      label="Submit enquiry only (pay later after final quote)"
                      value="enquiry_only"
                      checked={paymentMethod === 'enquiry_only'}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                    />
                    <Form.Check
                      type="radio"
                      id="wholesale-online-advance"
                      name="wholesale-payment-method"
                      label="Submit enquiry + pay online advance now"
                      value="online_advance"
                      checked={paymentMethod === 'online_advance'}
                      onChange={(e) => setPaymentMethod(e.target.value)}
                      className="mt-2"
                    />
                  </div>
                </Form.Group>

                <Button type="submit" variant="success" className="w-100" disabled={loading}>
                  {loading
                    ? 'Processing...'
                    : paymentMethod === 'online_advance'
                    ? 'Submit & Pay Advance'
                    : 'Submit Enquiry'}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Card className="shadow-sm">
        <Card.Body>
          <Card.Title className="fw-bold mb-3">Sample wholesale price tiers</Card.Title>
          <Table bordered responsive>
            <thead>
              <tr>
                <th>Quantity (boxes)</th>
                <th>Approx. discount</th>
                <th>Ideal for</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>50 – 99</td>
                <td>Up to 10% off</td>
                <td>Small offices, birthday parties</td>
              </tr>
              <tr>
                <td>100 – 249</td>
                <td>10–18% off</td>
                <td>Corporate gifting, mid‑size events</td>
              </tr>
              <tr>
                <td>250+</td>
                <td>Custom pricing</td>
                <td>Large events, reseller partners</td>
              </tr>
            </tbody>
          </Table>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default WholesalePage;


