import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, Table, Alert, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../CartContext';
import api from '../api';
import analytics from '../services/analyticsService';

const CartPage = () => {
  const navigate = useNavigate();
  const { items, updateQuantity, removeFromCart, clearCart, total } = useCart();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [showAddressModal, setShowAddressModal] = useState(false);
  const [razorpayOrder, setRazorpayOrder] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('razorpay');
  const [address, setAddress] = useState({
    shipping_address: '',
    phone_number: ''
  });
  const [discountCode, setDiscountCode] = useState('');
  const [appliedDiscount, setAppliedDiscount] = useState(null);
  const [discountError, setDiscountError] = useState(null);

  useEffect(() => {
    analytics.trackPurchasePageView();
  }, []);

  const handleApplyDiscount = async () => {
    if (!discountCode) return;
    try {
      setLoading(true);
      setDiscountError(null);
      const response = await api.post('discounts/validate/', { code: discountCode });
      setAppliedDiscount(response.data);
      analytics.track('discount_applied', {
        code: discountCode,
        percentage: response.data.discount_percentage
      });
    } catch (error) {
      setDiscountError(error.response?.data?.error || 'Invalid discount code');
      setAppliedDiscount(null);
    } finally {
      setLoading(false);
    }
  };

  const discountedTotal = appliedDiscount 
    ? total * (1 - appliedDiscount.discount_percentage / 100)
    : total;

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

  const createRazorpayOrder = async () => {
    try {
      const response = await api.post('razorpay/create-order/', {
        amount: total,
        discount_code: appliedDiscount?.code
      });
      return response.data;
    } catch (error) {
      const backendMessage = error.response?.data?.error;
      throw new Error(backendMessage || 'Failed to create payment order');
    }
  };

  const verifyPayment = async (paymentData) => {
    try {
      const response = await api.post('razorpay/verify-payment/', paymentData);
      return response.data;
    } catch (error) {
      throw new Error('Payment verification failed');
    }
  };

  const createOrder = async ({ paymentId = null, method = 'razorpay' }) => {
    try {
      const orderData = {
        ...(paymentId ? { payment_id: paymentId } : {}),
        payment_method: method,
        discount_code: appliedDiscount?.code,
        items: items.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        })),
        shipping_address: address.shipping_address,
        phone_number: address.phone_number
      };

      const response = await api.post('create-order/', orderData);
      return response.data;
    } catch (error) {
      throw new Error('Failed to create order');
    }
  };

  const handleCheckout = async () => {
    if (!items.length) return;
    
    analytics.track('purchase_initiated', {
      cart_value: total,
      discounted_value: discountedTotal,
      discount_code: appliedDiscount?.code,
      cart_items_count: items.length,
      products: items.map(item => ({
        id: item.id,
        name: item.name,
        price: item.price,
        quantity: item.quantity
      }))
    });
    
    setShowAddressModal(true);
  };

  const handlePayment = async () => {
    if (!address.shipping_address || !address.phone_number) {
      setError('Please provide shipping address and phone number');
      return;
    }

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      if (paymentMethod === 'cod') {
        await createOrder({ method: 'cod' });

        analytics.track('purchase_completed', {
          total_value: discountedTotal,
          original_value: total,
          discount_applied: appliedDiscount?.discount_percentage || 0,
          items_purchased: items.length,
          purchase_method: 'cod',
        });

        clearCart();
        setMessage('Order placed with Cash on Delivery. Your cookies are on their way!');
        setShowAddressModal(false);
        setLoading(false);
        setTimeout(() => navigate('/dashboard'), 2500);
        return;
      }

      const razorpayLoaded = await loadRazorpayScript();
      if (!razorpayLoaded) {
        setError('Failed to load payment gateway.');
        setLoading(false);
        return;
      }

      const orderData = await createRazorpayOrder();
      setRazorpayOrder(orderData);

      const options = {
        key: orderData.key_id,
        amount: Math.round(orderData.amount * 100), 
        currency: 'INR',
        name: 'CookieCrave',
        description: appliedDiscount ? `Discount Applied: ${appliedDiscount.discount_percentage}%` : 'Purchase of delicious cookies',
        order_id: orderData.razorpay_order_id,
        handler: async function (response) {
          try {
            await verifyPayment({
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature
            });

            await createOrder({
              paymentId: orderData.payment_id,
              method: 'razorpay',
            });

            analytics.track('purchase_completed', {
              total_value: discountedTotal,
              original_value: total,
              discount_applied: appliedDiscount?.discount_percentage || 0,
              items_purchased: items.length,
              purchase_method: 'razorpay',
            });

            clearCart();
            setMessage('Payment successful! Your cookies are on their way!');
            setShowAddressModal(false);
            setTimeout(() => navigate('/dashboard'), 2500);
          } catch (error) {
            console.error('Payment Error:', error);
            setError(error.message || 'Payment processing failed.');
          } finally {
            setLoading(false);
          }
        },
        modal: {
          ondismiss: function() {
            setError('Payment was cancelled.');
            setLoading(false);
          }
        },
        prefill: {
          contact: address.phone_number,
        }
      };

      const rzp = new window.Razorpay(options);
      rzp.open();

    } catch (error) {
      setError(error.message || 'Error initiating payment.');
      setLoading(false);
    }
  };

  return (
    <Container>
      <h2 className="mb-4 fw-bold">Your Cart</h2>
      {message && <Alert variant="success">{message}</Alert>}
      {error && <Alert variant="danger">{error}</Alert>}
      {items.length === 0 ? (
        <Card>
          <Card.Body>
            <Card.Text>Your cart is empty. Add some delicious cookies!</Card.Text>
          </Card.Body>
        </Card>
      ) : (
        <Row>
          <Col md={8}>
            <Table striped bordered hover responsive>
              <thead>
                <tr>
                  <th>Cookie</th>
                  <th>Price</th>
                  <th>Quantity</th>
                  <th>Subtotal</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {items.map(item => (
                  <tr key={item.id}>
                    <td>{item.name}</td>
                    <td>₹{item.price}</td>
                    <td style={{ maxWidth: '100px' }}>
                      <Form.Control
                        type="number"
                        min="1"
                        value={item.quantity}
                        onChange={(e) =>
                          updateQuantity(item.id, Number(e.target.value) || 1)
                        }
                      />
                    </td>
                    <td>₹{(Number(item.price) * item.quantity).toFixed(2)}</td>
                    <td>
                      <Button
                        variant="outline-danger"
                        size="sm"
                        onClick={() => removeFromCart(item.id)}
                      >
                        Remove
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Col>
          <Col md={4}>
            <Card className="border-0 shadow-sm" style={{ borderRadius: '15px' }}>
              <Card.Body className="p-4">
                <h5 className="fw-bold mb-4">Order Summary</h5>
                
                {/* Discount Code Section */}
                <div className="mb-4">
                  <Form.Label className="small fw-bold text-muted">DISCOUNT CODE</Form.Label>
                  <div className="d-flex gap-2">
                    <Form.Control
                      type="text"
                      placeholder="Enter code"
                      value={discountCode}
                      onChange={(e) => setDiscountCode(e.target.value.toUpperCase())}
                      disabled={appliedDiscount}
                      className="rounded-pill"
                    />
                    {!appliedDiscount ? (
                      <Button 
                        variant="dark" 
                        onClick={handleApplyDiscount}
                        disabled={loading || !discountCode}
                        className="rounded-pill px-4"
                      >
                        Apply
                      </Button>
                    ) : (
                      <Button 
                        variant="outline-danger" 
                        onClick={() => {
                          setAppliedDiscount(null);
                          setDiscountCode('');
                        }}
                        className="rounded-pill px-4"
                      >
                        Remove
                      </Button>
                    )}
                  </div>
                  {discountError && <div className="text-danger small mt-1 ms-2">{discountError}</div>}
                  {appliedDiscount && (
                    <div className="text-success small mt-1 ms-2 fw-bold">
                      ✓ {appliedDiscount.discount_percentage}% discount applied!
                    </div>
                  )}
                </div>

                <hr className="my-4" />

                <div className="d-flex justify-content-between mb-2">
                  <span>Subtotal</span>
                  <span>₹{total.toFixed(2)}</span>
                </div>

                {appliedDiscount && (
                  <div className="d-flex justify-content-between mb-2 text-success fw-bold">
                    <span>Discount ({appliedDiscount.discount_percentage}%)</span>
                    <span>-₹{(total - discountedTotal).toFixed(2)}</span>
                  </div>
                )}

                <div className="d-flex justify-content-between mb-4 mt-3">
                  <span className="h5 fw-bold">Total</span>
                  <span className="h5 fw-bold text-primary">₹{discountedTotal.toFixed(2)}</span>
                </div>

                <div className="d-grid gap-2">
                  <Button
                    variant="success"
                    size="lg"
                    className="rounded-pill fw-bold"
                    onClick={handleCheckout}
                    disabled={loading || !items.length}
                  >
                    {loading ? 'Processing...' : 'Proceed to Checkout'}
                  </Button>
                  <Button
                    variant="link"
                    className="text-muted text-decoration-none small"
                    onClick={clearCart}
                    disabled={loading}
                  >
                    Clear My Cart
                  </Button>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {/* Address Modal */}
      <Modal show={showAddressModal} onHide={() => setShowAddressModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Shipping Information</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group className="mb-3">
            <Form.Label>Payment Method</Form.Label>
            <div>
              <Form.Check
                type="radio"
                id="payment-razorpay"
                name="payment-method"
                label="Online Payment (Razorpay)"
                value="razorpay"
                checked={paymentMethod === 'razorpay'}
                onChange={(e) => setPaymentMethod(e.target.value)}
              />
              <Form.Check
                type="radio"
                id="payment-cod"
                name="payment-method"
                label="Cash on Delivery"
                value="cod"
                checked={paymentMethod === 'cod'}
                onChange={(e) => setPaymentMethod(e.target.value)}
                className="mt-2"
              />
            </div>
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Shipping Address</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              placeholder="Enter your complete shipping address"
              value={address.shipping_address}
              onChange={(e) => setAddress({...address, shipping_address: e.target.value})}
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Phone Number</Form.Label>
            <Form.Control
              type="tel"
              placeholder="Enter your phone number"
              value={address.phone_number}
              onChange={(e) => setAddress({...address, phone_number: e.target.value})}
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowAddressModal(false)}>
            Cancel
          </Button>
          <Button variant="success" onClick={handlePayment} disabled={loading}>
            {loading ? 'Processing...' : paymentMethod === 'cod'
              ? `Place Order (COD ₹${discountedTotal.toFixed(2)})`
              : `Pay ₹${discountedTotal.toFixed(2)}`}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default CartPage;

