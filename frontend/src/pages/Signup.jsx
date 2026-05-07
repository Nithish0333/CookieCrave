import React, { useState } from 'react';
import { Form, Button, Card, Container, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import api from '../api';

const Signup = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [retypePassword, setRetypePassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (password !== retypePassword) {
            setError('Passwords do not match');
            return;
        }

        try {
            await api.post('users/register/', { username, email, password });
            window.location.href = '/login';
        } catch (err) {
            setError(err.response?.data?.detail || 'Error creating account. Username might already exist.');
        }
    };

    return (
        <Container className="d-flex align-items-center justify-content-center" style={{ minHeight: '80vh' }}>
            <Card style={{ maxWidth: '400px', width: '100%' }} className="p-4 auth-card-animate">
                <Card.Body>
                    <div className="text-center mb-4">
                        <span className="cookie-icon" style={{ fontSize: '3rem' }}>🎉</span>
                        <h2 className="fw-bold mt-2">Create Account</h2>
                    </div>
                    {error && <Alert variant="danger">{error}</Alert>}
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" value={username} onChange={e => setUsername(e.target.value)} required />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Email</Form.Label>
                            <Form.Control type="email" value={email} onChange={e => setEmail(e.target.value)} required />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>New Password</Form.Label>
                            <Form.Control type="password" value={password} onChange={e => setPassword(e.target.value)} required />
                        </Form.Group>
                        <Form.Group className="mb-4">
                            <Form.Label>Retype Password</Form.Label>
                            <Form.Control type="password" value={retypePassword} onChange={e => setRetypePassword(e.target.value)} required />
                        </Form.Group>
                        <Button variant="primary" type="submit" className="w-100 mb-3">Sign Up</Button>
                        
                        <div className="text-center small">
                            Already have an account? <Link to="/login" className="auth-link">Login Here</Link>
                        </div>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default Signup;
