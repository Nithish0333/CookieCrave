import React, { useState } from 'react';
import { Modal, Form, Button, Alert } from 'react-bootstrap';
import api from '../api';

const ForgotPasswordModal = ({ show, onHide }) => {
    // State management
    const [step, setStep] = useState(1); // 1 = email entry, 2 = verification & reset
    const [email, setEmail] = useState('');
    const [verificationCode, setVerificationCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [retypedPassword, setRetypedPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);

    // Reset state when modal opens/closes
    React.useEffect(() => {
        if (show) {
            // Reset when modal opens
            setStep(1);
            setEmail('');
            setVerificationCode('');
            setNewPassword('');
            setConfirmPassword('');
            setRetypedPassword('');
            setError('');
            setSuccess('');
        }
    }, [show]);

    const handleEmailSubmit = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        setLoading(true);
        setError('');
        setSuccess('');

        try {
            const response = await api.post('users/forgot-password/', { email });
            
            if (response.data.verification_code_sent) {
                setSuccess('Verification code sent! Please check your email.');
                setStep(2);
            } else {
                setSuccess(response.data.detail || 'Reset link sent to your email!');
                setStep(2);
            }
        } catch (err) {
            console.error('Forgot password error:', err.response?.data);
            setError(err.response?.data?.detail || 'Error sending reset link. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleResetSubmit = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        setLoading(true);
        setError('');

        // Validation
        if (!verificationCode || !newPassword || !confirmPassword || !retypedPassword) {
            setError('All fields are required.');
            setLoading(false);
            return;
        }

        if (newPassword.length < 8) {
            setError('Password must be at least 8 characters long.');
            setLoading(false);
            return;
        }

        if (newPassword !== confirmPassword) {
            setError('New password and confirm password do not match.');
            setLoading(false);
            return;
        }

        if (newPassword !== retypedPassword) {
            setError('Password and retype password do not match.');
            setLoading(false);
            return;
        }

        try {
            const response = await api.post('users/reset-password-with-code/', {
                email: email,
                verification_code: verificationCode,
                password: newPassword,
                confirm_password: confirmPassword,
                retyped_password: retypedPassword
            });

            setSuccess(`Password reset successful! Your new password "${newPassword}" is now active. Use username "nithish" to login.`);
            // Don't auto-close - let user see the message and close manually
            // setTimeout(() => {
            //     onHide(); // Close modal after success
            //     setStep(1); // Reset for next time
            // }, 3000); // Give more time to read the message
        } catch (err) {
            console.error('Reset password error:', err.response?.data);
            setError(err.response?.data?.detail || 'Error resetting password. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleBack = () => {
        setStep(1);
        setError('');
        setSuccess('');
    };

    const handleCancel = () => {
        onHide();
    };

    return (
        <Modal 
            show={show} 
            onHide={handleCancel}
            centered
            backdrop="static"
            keyboard={false}
            size="lg"
        >
            <Modal.Header closeButton>
                <Modal.Title>
                    {step === 1 ? 'Reset Password' : 'Enter Verification Code & New Password'}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {success && (
    <Alert variant="success" className="mb-3">
                    <div>
                        <strong>✅ Password Reset Successful!</strong>
                        <div className="mt-2">
                            <small>
                                <strong>Your new password:</strong> <code>{newPassword}</code>
                                <br />
                                <strong>Username for login:</strong> <code>nithish</code>
                                <br />
                                <strong>Important:</strong> Use username (not email) to login.
                            </small>
                        </div>
                        <div className="mt-3">
                            <Button variant="success" size="sm" onClick={() => {
                                onHide();
                                window.location.href = '/login';
                            }}>
                                Go to Login
                            </Button>
                        </div>
                    </div>
                </Alert>
            )}
                {error && <Alert variant="danger" className="mb-3">{error}</Alert>}
                
                {step === 1 ? (
                    // Step 1: Email entry
                    <Form onSubmit={handleEmailSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Enter your email address</Form.Label>
                            <Form.Control 
                                type="email" 
                                placeholder="your@email.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                autoFocus
                            />
                        </Form.Group>
                        <Button 
                            variant="primary" 
                            type="submit" 
                            className="w-100"
                            disabled={loading}
                        >
                            {loading ? 'Sending...' : 'Send Verification Code'}
                        </Button>
                    </Form>
                ) : (
                    // Step 2: Verification code and password reset
                    <Form onSubmit={handleResetSubmit}>
                        <Alert variant="info" className="mb-3">
                            <strong>Email:</strong> {email}
                            <br />
                            <small>Check your inbox for 6-digit verification code</small>
                        </Alert>
                        
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
                                autoFocus
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
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                required
                                minLength={8}
                            />
                            <Form.Text className="text-muted">
                                Password must be at least 8 characters long.
                            </Form.Text>
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Form.Label>Confirm Password</Form.Label>
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

                        <div className="d-flex gap-2">
                            <Button 
                                variant="secondary" 
                                onClick={handleBack}
                                className="flex-fill"
                            >
                                Back
                            </Button>
                            <Button 
                                variant="primary" 
                                type="submit" 
                                className="flex-fill"
                                disabled={loading}
                            >
                                {loading ? 'Resetting...' : 'Reset Password'}
                            </Button>
                        </div>
                    </Form>
                )}
            </Modal.Body>
        </Modal>
    );
};

export default ForgotPasswordModal;
