import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Alert, Row, Col, ProgressBar } from 'react-bootstrap';
import api from '../api';
import './SellerRegisterModal.css';

const SellerRegisterModal = ({ show, onHide, onSecondarySuccess }) => {
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    
    // Form data
    const [formData, setFormData] = useState({
        business_name: '',
        description: '',
        phone_number: '',
        address: ''
    });
    
    // OTP data
    const [otpCode, setOtpCode] = useState('');
    const [resendCooldown, setResendCooldown] = useState(0);

    useEffect(() => {
        let timer;
        if (resendCooldown > 0) {
            timer = setTimeout(() => setResendCooldown(resendCooldown - 1), 1000);
        }
        return () => clearTimeout(timer);
    }, [resendCooldown]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const res = await api.post('users/seller-profile/', formData);
            if (res.data.requires_verification) {
                setStep(3);
            } else {
                setSuccess('Profile updated successfully!');
                onSecondarySuccess();
                setTimeout(onHide, 2000);
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleVerify = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            await api.post('users/seller-profile/verify/', { code: otpCode });
            setSuccess('Welcome abroad! You are now a verified seller.');
            setStep(4);
            onSecondarySuccess();
        } catch (err) {
            setError(err.response?.data?.detail || 'Invalid verification code.');
        } finally {
            setLoading(false);
        }
    };

    const handleResend = async () => {
        if (resendCooldown > 0) return;
        setLoading(true);
        try {
            await api.post('users/seller-profile/resend-otp/');
            setResendCooldown(60);
            setSuccess('A new code has been sent.');
            setTimeout(() => setSuccess(null), 3000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to resend code.');
        } finally {
            setLoading(false);
        }
    };

    const renderStep = () => {
        switch (step) {
            case 1:
                return (
                    <div className="text-center p-4">
                        <div className="onboarding-img-container mb-4">
                            <img src="/seller_onboarding_illustration.png" alt="Seller Onboarding" className="img-fluid rounded-3 shadow-sm" style={{maxHeight: '200px'}} />
                        </div>
                        <h3 className="fw-bold mb-3">Start Your Cookie Journey</h3>
                        <p className="text-muted mb-4 text-balanced">
                            Turn your passion for baking into a business. Reach thousands of cookie lovers across the country.
                        </p>
                        <ul className="text-start mb-4 mx-auto" style={{maxWidth: '300px'}}>
                            <li><i className="bi bi-check-circle-fill text-success me-2"></i> Low platform fees</li>
                            <li><i className="bi bi-check-circle-fill text-success me-2"></i> Easy listing management</li>
                            <li><i className="bi bi-check-circle-fill text-success me-2"></i> Secure payments</li>
                        </ul>
                        <Button variant="danger" className="w-100 py-2 fw-bold" onClick={() => setStep(2)}>
                            Get Started
                        </Button>
                    </div>
                );
            case 2:
                return (
                    <div className="p-3">
                        <h4 className="fw-bold mb-4">Business Details</h4>
                        <Form onSubmit={handleRegister}>
                            <Form.Group className="mb-3">
                                <Form.Label className="small fw-bold">Business Name</Form.Label>
                                <Form.Control 
                                    name="business_name"
                                    value={formData.business_name}
                                    onChange={handleInputChange}
                                    required 
                                    placeholder="e.g. Grandma's Secrets" 
                                    className="premium-input"
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label className="small fw-bold">Description</Form.Label>
                                <Form.Control 
                                    as="textarea"
                                    rows={2}
                                    name="description"
                                    value={formData.description}
                                    onChange={handleInputChange}
                                    placeholder="Tell your story..." 
                                    className="premium-input"
                                />
                            </Form.Group>
                            <Form.Group className="mb-3">
                                <Form.Label className="small fw-bold">Phone Number (10 digits)</Form.Label>
                                <Form.Control 
                                    type="tel"
                                    name="phone_number"
                                    value={formData.phone_number}
                                    onChange={handleInputChange}
                                    required 
                                    placeholder="9876543210" 
                                    className="premium-input"
                                />
                                <Form.Text className="text-muted">We'll send an OTP to verify.</Form.Text>
                            </Form.Group>
                            <Form.Group className="mb-4">
                                <Form.Label className="small fw-bold">Business Address</Form.Label>
                                <Form.Control 
                                    type="text"
                                    name="address"
                                    value={formData.address}
                                    onChange={handleInputChange}
                                    placeholder="Pickup location for orders" 
                                    className="premium-input"
                                />
                            </Form.Group>
                            <div className="d-flex gap-2">
                                <Button variant="light" className="flex-fill fw-bold" onClick={() => setStep(1)} disabled={loading}>
                                    Back
                                </Button>
                                <Button variant="danger" type="submit" className="flex-grow-2 fw-bold" disabled={loading}>
                                    {loading ? 'Sending OTP...' : 'Continue'}
                                </Button>
                            </div>
                        </Form>
                    </div>
                );
            case 3:
                return (
                    <div className="text-center p-3">
                        <div className="mb-4">
                            <i className="bi bi-shield-check display-4 text-danger"></i>
                        </div>
                        <h4 className="fw-bold mb-2">Verify Phone</h4>
                        <p className="text-muted mb-4 small">
                            We've sent a 6-digit code to <strong>{formData.phone_number}</strong>
                        </p>
                        <Form onSubmit={handleVerify}>
                            <Form.Group className="mb-4">
                                <Form.Control 
                                    type="text"
                                    value={otpCode}
                                    onChange={(e) => setOtpCode(e.target.value)}
                                    maxLength={6}
                                    required
                                    placeholder="000000"
                                    className="otp-input text-center display-6 fw-bold"
                                />
                            </Form.Group>
                            <Button variant="danger" type="submit" className="w-100 py-2 fw-bold mb-3" disabled={loading}>
                                {loading ? 'Verifying...' : 'Complete Verification'}
                            </Button>
                            <Button 
                                variant="link" 
                                className="text-muted text-decoration-none small" 
                                onClick={handleResend}
                                disabled={loading || resendCooldown > 0}
                            >
                                {resendCooldown > 0 ? `Resend in ${resendCooldown}s` : "Didn't receive code? Resend"}
                            </Button>
                        </Form>
                    </div>
                );
            case 4:
                return (
                    <div className="text-center p-5">
                        <div className="success-animation mb-4">
                            <i className="bi bi-party-fill display-1 text-success pulse"></i>
                        </div>
                        <h3 className="fw-bold mb-2">You're All Set!</h3>
                        <p className="text-muted mb-4">
                            Your seller profile is now active. Head over to your dashboard to list your first cookie.
                        </p>
                        <Button variant="success" className="w-100 py-2 fw-bold" onClick={onHide}>
                            Go to Dashboard
                        </Button>
                    </div>
                );
            default:
                return null;
        }
    };

    const progress = (step / 4) * 100;

    return (
        <Modal 
            show={show} 
            onHide={onHide} 
            centered 
            className="seller-modal"
            backdrop="static"
        >
            <Modal.Header closeButton className="border-0 pb-0">
                <div className="w-100 pe-4">
                    <ProgressBar now={progress} variant="danger" style={{height: '4px'}} className="mt-3" />
                </div>
            </Modal.Header>
            <Modal.Body className="pt-0">
                {error && <Alert variant="danger" className="py-2 small mx-3 mb-0 mt-2">{error}</Alert>}
                {success && step !== 4 && <Alert variant="success" className="py-2 small mx-3 mb-0 mt-2">{success}</Alert>}
                {renderStep()}
            </Modal.Body>
        </Modal>
    );
};

export default SellerRegisterModal;
