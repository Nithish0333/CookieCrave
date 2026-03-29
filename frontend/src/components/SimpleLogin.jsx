import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const SimpleLogin = () => {
    const [username, setUsername] = useState('nithish');
    const [password, setPassword] = useState('newtestpass123');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess('');

        console.log('=== SIMPLE LOGIN TEST ===');
        console.log('Username:', username);
        console.log('Password:', password);
        console.log('Trying direct API call...');

        try {
            // Use direct axios call to bypass any API configuration issues
            const response = await axios.post('http://localhost:8000/api/users/login/', {
                username: username,
                password: password
            }, {
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            console.log('✅ Login Response:', response.data);
            console.log('✅ Status:', response.status);
            console.log('✅ Access Token:', response.data.access ? 'Received' : 'Missing');
            console.log('✅ Refresh Token:', response.data.refresh ? 'Received' : 'Missing');

            // Store tokens
            localStorage.setItem('access', response.data.access);
            localStorage.setItem('refresh', response.data.refresh);
            
            console.log('✅ Tokens stored in localStorage');
            setSuccess('✅ Login successful! Redirecting to home...');

            // Redirect to home
            setTimeout(() => {
                navigate('/home');
            }, 1000);

        } catch (err) {
            console.error('❌ Login Error:', err);
            console.error('❌ Error Response:', err.response?.data);
            console.error('❌ Error Status:', err.response?.status);
            console.error('❌ Error Message:', err.message);
            
            let errorMessage = 'Unknown error';
            if (err.response?.data?.detail) {
                errorMessage = err.response.data.detail;
            } else if (err.message) {
                errorMessage = err.message;
            } else if (err.code === 'ECONNREFUSED') {
                errorMessage = 'Cannot connect to backend server. Is it running?';
            } else if (err.code === 'ERR_NETWORK') {
                errorMessage = 'Network error. Check backend server.';
            }
            
            setError(`❌ Login failed: ${errorMessage}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card">
                        <div className="card-header">
                            <h3>Simple Login Test</h3>
                        </div>
                        <div className="card-body">
                            {success && <Alert variant="success">{success}</Alert>}
                            {error && <Alert variant="danger">{error}</Alert>}
                            
                            <Form onSubmit={handleLogin}>
                                <Form.Group className="mb-3">
                                    <Form.Label>Username</Form.Label>
                                    <Form.Control
                                        type="text"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                        placeholder="Enter username"
                                        required
                                    />
                                    <Form.Text className="text-muted">
                                        Use: <strong>nithish</strong>
                                    </Form.Text>
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        placeholder="Enter password"
                                        required
                                    />
                                    <Form.Text className="text-muted">
                                        Use: <strong>newtestpass123</strong>
                                    </Form.Text>
                                </Form.Group>

                                <Button variant="primary" type="submit" disabled={loading} className="w-100">
                                    {loading ? 'Logging in...' : 'Login'}
                                </Button>
                            </Form>

                            <div className="mt-3">
                                <small className="text-muted">
                                    <strong>Test Credentials:</strong><br/>
                                    Username: nithish<br/>
                                    Password: newtestpass123
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SimpleLogin;
