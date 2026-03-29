import React, { useState } from 'react';
import { Form, Button, Card, Container, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import api from '../api';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [rememberMe, setRememberMe] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await api.post('users/login/', { username, password });
            const storage = rememberMe ? localStorage : sessionStorage;
            // Clear both first to avoid stale tokens
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            sessionStorage.removeItem('access');
            sessionStorage.removeItem('refresh');
            
            storage.setItem('access', res.data.access);
            storage.setItem('refresh', res.data.refresh);
            window.location.href = '/dashboard';
        } catch (err) {
            setError('Invalid credentials');
        }
    };

    const handleForgotPassword = () => {
        alert("Password reset link sent to your email! (Demo)");
    };

    return (
        <Container className="d-flex align-items-center justify-content-center" style={{ minHeight: '80vh' }}>
            <Card style={{ maxWidth: '400px', width: '100%' }} className="p-4 auth-card-animate">
                <Card.Body>
                    <div className="text-center mb-4">
                        <span className="cookie-icon" style={{ fontSize: '3rem' }}>🍪</span>
                        <h2 className="fw-bold mt-2">Welcome Back</h2>
                    </div>
                    {error && <Alert variant="danger">{error}</Alert>}
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" value={username} onChange={e => setUsername(e.target.value)} required />
                        </Form.Group>
                        <Form.Group className="mb-2">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" value={password} onChange={e => setPassword(e.target.value)} required />
                        </Form.Group>
                        
                        <div className="d-flex justify-content-between align-items-center mb-4 text-muted small">
                            <Form.Check 
                                type="checkbox" 
                                label="Remember me" 
                                checked={rememberMe}
                                onChange={(e) => setRememberMe(e.target.checked)}
                            />
                            <span 
                                className="auth-link" 
                                style={{cursor: 'pointer'}} 
                                onClick={handleForgotPassword}
                            >
                                Forgot Password?
                            </span>
                        </div>

                        <Button variant="primary" type="submit" className="w-100 mb-3">Login</Button>
                        
                        <div className="text-center small">
                            Don't have an account? <Link to="/signup" className="auth-link">Sign Up</Link>
                        </div>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default Login;
