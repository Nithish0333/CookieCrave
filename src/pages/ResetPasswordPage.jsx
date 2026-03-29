import React, { useState, useEffect } from 'react';
import { Form, Button, Alert, Card, InputGroup } from 'react-bootstrap';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import api from '../api';
import './AuthPage.css';

const ResetPasswordPage = () => {
    const { uidb64, token } = useParams();
    const location = useLocation();
    const navigate = useNavigate();
    
    // Get verification code from URL query params
    const urlCode = new URLSearchParams(location.search).get('code');
    
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [retypedPassword, setRetypedPassword] = useState('');
    const [verificationCode, setVerificationCode] = useState(urlCode || '');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);
    const [isValidating, setIsValidating] = useState(true);
    const [linkValid, setLinkValid] = useState(null);

    useEffect(() => {
        // Validate the reset link when component mounts
        const validateLink = async () => {
            try {
                // We can validate by making a test request or just check if parameters exist
                if (uidb64 && token) {
                    setLinkValid(true);
                } else {
                    setLinkValid(false);
                    setError('Invalid reset link. Please request a new password reset.');
                }
            } catch (err) {
                setLinkValid(false);
                setError('Invalid reset link. Please request a new password reset.');
            } finally {
                setIsValidating(false);
            }
        };

        validateLink();
    }, [uidb64, token]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);

        // Validation
        if (!password || !confirmPassword || !retypedPassword) {
            setError('All password fields are required.');
            setLoading(false);
            return;
        }

        if (password.length < 8) {
            setError('Password must be at least 8 characters long.');
            setLoading(false);
            return;
        }

        if (password !== confirmPassword) {
            setError('New password and confirm password do not match.');
            setLoading(false);
            return;
        }

        if (password !== retypedPassword) {
            setError('Password and retype password do not match.');
            setLoading(false);
            return;
        }

        try {
            const response = await api.post(`users/reset-password/${uidb64}/${token}/`, {
                password: password,
                confirm_password: confirmPassword,
                retyped_password: retypedPassword,
                verification_code: verificationCode
            });

            setSuccess('Password reset successful! Redirecting to login...');
            setTimeout(() => {
                navigate('/login');
            }, 2000);
        } catch (err) {
            console.error('Reset password error:', err.response?.data);
            setError(err.response?.data?.detail || 'Error resetting password. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (isValidating) {
        return (
            <div className="d-flex justify-content-center align-items-center min-vh-100">
                <Card className="p-4 shadow-sm auth-card-animate" style={{ minWidth: '400px' }}>
                    <div className="text-center">
                        <div className="spinner-border text-primary" role="status">
                            <span className="visually-hidden">Validating...</span>
                        </div>
                        <p className="mt-3 text-muted">Validating reset link...</p>
                    </div>
                </Card>
            </div>
        );
    }

    if (linkValid === false) {
        return (
            <div className="d-flex justify-content-center align-items-center min-vh-100">
                <Card className="p-4 shadow-sm auth-card-animate" style={{ minWidth: '400px' }}>
                    <div className="text-center">
                        <h4 className="text-danger mb-3">Invalid Reset Link</h4>
                        <p className="text-muted mb-4">
                            {error || 'This password reset link is invalid or has expired.'}
                        </p>
                        <Button 
                            variant="primary" 
                            onClick={() => navigate('/login')}
                            className="w-100"
                        >
                            Back to Login
                        </Button>
                    </div>
                </Card>
            </div>
        );
    }

    return (
        <div className="d-flex justify-content-center align-items-center min-vh-100">
            <Card className="p-4 shadow-sm auth-card-animate" style={{ minWidth: '450px', maxWidth: '500px' }}>
                <Card.Body>
                    <div className="text-center mb-4">
                        <h3 className="fw-bold">Reset Password</h3>
                        <p className="text-muted">Enter your new password below</p>
                    </div>

                    {success && <Alert variant="success" className="mb-3">{success}</Alert>}
                    {error && <Alert variant="danger" className="mb-3">{error}</Alert>}

                    {urlCode && (
                        <Alert variant="info" className="mb-3">
                            <strong>Verification Code:</strong> {urlCode}
                            <br />
                            <small>This code was included in your reset link for your convenience.</small>
                        </Alert>
                    )}

                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Verification Code (from email)</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Enter 6-digit code"
                                value={verificationCode}
                                onChange={(e) => setVerificationCode(e.target.value)}
                                maxLength={6}
                                pattern="[0-9]{6}"
                                required
                            />
                            <Form.Text className="text-muted">
                                Enter the 6-digit verification code sent to your email
                            </Form.Text>
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Form.Label>New Password</Form.Label>
                            <Form.Control
                                type="password"
                                placeholder="Enter new password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                minLength={8}
                            />
                            <Form.Text className="text-muted">
                                Password must be at least 8 characters long.
                            </Form.Text>
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Form.Label>Confirm New Password</Form.Label>
                            <Form.Control
                                type="password"
                                placeholder="Confirm new password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                                minLength={8}
                            />
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Form.Label>Retype Password</Form.Label>
                            <Form.Control
                                type="password"
                                placeholder="Retype new password for verification"
                                value={retypedPassword}
                                onChange={(e) => setRetypedPassword(e.target.value)}
                                required
                                minLength={8}
                            />
                            <Form.Text className="text-muted">
                                Retype your new password to confirm accuracy
                            </Form.Text>
                        </Form.Group>

                        <Button
                            variant="primary"
                            type="submit"
                            className="w-100 fw-bold"
                            disabled={loading}
                        >
                            {loading ? 'Resetting...' : 'Reset Password'}
                        </Button>

                        <div className="text-center mt-3">
                            <Button
                                variant="link"
                                onClick={() => navigate('/login')}
                                className="text-muted"
                            >
                                Back to Login
                            </Button>
                        </div>
                    </Form>
                </Card.Body>
            </Card>
        </div>
    );
};

export default ResetPasswordPage;
