import React, { useState } from 'react';
import { Form, Button, Alert, Modal } from 'react-bootstrap';
import { useNavigate, useLocation } from 'react-router-dom';
import api from '../api';
import analytics from '../services/analyticsService';
import ForgotPasswordModal from '../components/ForgotPasswordModal';
import './AuthPage.css';

const AuthPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    
    // Determine initial state based on route
    const isInitialSignup = location.pathname === '/signup';
    const [isRightPanelActive, setIsRightPanelActive] = useState(isInitialSignup);
    
    // Forgot Password Modal State
    const [showForgotPassword, setShowForgotPassword] = useState(false);

    // Login State
    const [loginUsername, setLoginUsername] = useState('');
    const [loginPassword, setLoginPassword] = useState('');
    const [rememberMe, setRememberMe] = useState(false);
    const [loginError, setLoginError] = useState('');
    const [loginRedirect, setLoginRedirect] = useState('');

    // Signup State
    const [signupUsername, setSignupUsername] = useState('');
    const [signupEmail, setSignupEmail] = useState('');
    const [signupPassword, setSignupPassword] = useState('');
    const [signupRetypePassword, setSignupRetypePassword] = useState('');
    const [signupError, setSignupError] = useState('');
    const [signupSuccess, setSignupSuccess] = useState('');


    const switchToSignup = () => {
        console.log('Switching to signup panel');
        setIsRightPanelActive(true);
    };

    const switchToLogin = () => {
        console.log('Switching to login panel');
        setIsRightPanelActive(false);
        setLoginError('');
        setLoginRedirect('');
    };

    const handleLoginSubmit = async (e) => {
        e.preventDefault();
        console.log('Login attempt with:', loginUsername);
        
        try {
            console.log('Attempting login with:', { username: loginUsername, password: '***' });
            const res = await api.post('users/login/', { username: loginUsername, password: loginPassword });
            console.log('Login response:', res.data);
            console.log('Login successful');
            const storage = rememberMe ? localStorage : sessionStorage;
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            sessionStorage.removeItem('access');
            sessionStorage.removeItem('refresh');
            
            storage.setItem('access', res.data.access);
            storage.setItem('refresh', res.data.refresh);
            console.log('Tokens stored, navigating to home');
            navigate('/home');
        } catch (err) {
            console.error('Login failed:', err.response?.status, err.response?.data);
            console.error('Full error:', err);
            
            // Show error message but don't auto-redirect
            setLoginError(`Login failed: ${err.response?.data?.detail || 'Unknown error'}`);
            setLoginRedirect('');
            
            // Don't auto-switch to signup panel - let user try again
            // setTimeout(() => {
            //     setLoginRedirect('');
            //     setIsRightPanelActive(true);
            // }, 100);
        }
    };

    const handleSignupSubmit = async (e) => {
        e.preventDefault();
        if (signupPassword !== signupRetypePassword) {
            setSignupError('Passwords do not match');
            return;
        }
        try {
            await api.post('users/register/', { username: signupUsername, email: signupEmail, password: signupPassword });
            setSignupError('');
            setSignupSuccess('Account created successfully! Redirecting to login...');
            // Clear signup form
            setSignupUsername('');
            setSignupEmail('');
            setSignupPassword('');
            setSignupRetypePassword('');

            
            // Switch to login page after 2 seconds
            setTimeout(() => {
                setSignupSuccess('');
                switchToLogin();
                setLoginRedirect('Account created! Please login to continue.');
            }, 2000);
        } catch (err) {
            console.error('Signup error:', err.response?.data);
            const errorData = err.response?.data;
            let errorMessage = 'Error creating account.';
            
            if (errorData) {
                if (errorData.username) {
                    errorMessage = Array.isArray(errorData.username) ? errorData.username[0] : errorData.username;
                } else if (errorData.email) {
                    errorMessage = Array.isArray(errorData.email) ? errorData.email[0] : errorData.email;
                } else if (errorData.password) {
                    errorMessage = Array.isArray(errorData.password) ? errorData.password[0] : errorData.password;
                } else if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.non_field_errors) {
                    errorMessage = Array.isArray(errorData.non_field_errors) ? errorData.non_field_errors[0] : errorData.non_field_errors;
                }
            }
            
            setSignupError(errorMessage);
        }
    };

    const handleToggle = (isSignup) => {
        if (isSignup) {
            switchToSignup();
        } else {
            switchToLogin();
        }
        navigate(isSignup ? '/signup' : '/login', { replace: true });
    };

    return (
        <div className="auth-body">
            <div className={`auth-container ${isRightPanelActive ? "right-panel-active" : ""}`} id="auth-container">
                
                {/* SIGN UP CONTAINER */}
                <div className="form-container sign-up-container">
                    <Form onSubmit={handleSignupSubmit} className="auth-form">
                        <h2 className="auth-title">Create Account</h2>
                        {signupSuccess && <Alert variant="success" className="py-2 px-2 w-100 mb-3">{signupSuccess}</Alert>}
                        {signupError && <Alert variant="danger" className="py-1 px-2 w-100 mb-2">{signupError}</Alert>}
                        <Form.Control type="text" placeholder="Username" className="mb-2 auth-input" 
                            value={signupUsername} onChange={e => setSignupUsername(e.target.value)} required />
                        <Form.Control type="email" placeholder="Email" className="mb-2 auth-input" 
                            value={signupEmail} onChange={e => setSignupEmail(e.target.value)} required />
                        <Form.Control type="password" placeholder="Password" className="mb-2 auth-input" 
                            value={signupPassword} onChange={e => setSignupPassword(e.target.value)} required />
                        <Form.Control type="password" placeholder="Retype Password" className="mb-2 auth-input" 
                            value={signupRetypePassword} onChange={e => setSignupRetypePassword(e.target.value)} required />
                        

                        
                        <Button className="auth-btn" type="submit">Sign Up</Button>
                        <div className="mobile-toggle-btn d-md-none mt-3" onClick={() => handleToggle(false)}>
                            Already have an account? Login
                        </div>
                    </Form>
                </div>

                {/* LOGIN CONTAINER */}
                <div className="form-container sign-in-container">
                    <Form onSubmit={handleLoginSubmit} className="auth-form">
                        <h2 className="fw-bold mb-3">Login</h2>
                        {loginRedirect && <Alert variant="info" className="py-2 px-2 w-100 mb-3">{loginRedirect}</Alert>}
                        {loginError && <Alert variant="danger" className="py-1 px-2 w-100 mb-2">{loginError}</Alert>}
                        <Form.Control type="text" placeholder="Username" className="mb-3 auth-input" 
                            value={loginUsername} onChange={e => setLoginUsername(e.target.value)} required />
                        <Form.Control type="password" placeholder="Password" className="mb-3 auth-input" 
                            value={loginPassword} onChange={e => setLoginPassword(e.target.value)} required />
                        
                        <div className="d-flex justify-content-between align-items-center w-100 mb-3 px-2">
                            <Form.Check type="checkbox" label="Remember me" className="text-muted small"
                                checked={rememberMe} onChange={(e) => setRememberMe(e.target.checked)} />
                            <span className="text-muted small fw-bold" style={{cursor: 'pointer'}} 
                                onClick={() => setShowForgotPassword(true)}>
                                Forgot Password?
                            </span>
                        </div>

                        <Button className="auth-btn mt-2" type="submit">Login</Button>
                        <div className="mobile-toggle-btn d-md-none mt-3" onClick={() => handleToggle(true)}>
                            Don't have an account? Sign Up
                        </div>
                    </Form>
                </div>

                {/* OVERLAY CONTAINER */}
                <div className="overlay-container d-none d-md-block">
                    <div className="overlay">
                        <div className="overlay-panel overlay-left">
                            <img src="/logo.png" alt="Logo" style={{ width: '80px', marginBottom: '20px' }} />
                            <h2 className="fw-bold">Welcome Back!</h2>
                            <p>To keep connected with us please login with your personal info</p>
                            <Button className="auth-ghost-btn mt-3" onClick={() => handleToggle(false)}>Sign In</Button>
                        </div>
                        <div className="overlay-panel overlay-right">
                            <img src="/logo.png" alt="Logo" style={{ width: '80px', marginBottom: '20px' }} />
                            <h2 className="fw-bold">Hello, Friend!</h2>
                            <p>Enter your personal details and start your journey with CookieCrave</p>
                            <Button className="auth-ghost-btn mt-3" onClick={() => handleToggle(true)}>Sign Up</Button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Forgot Password Modal */}
            <ForgotPasswordModal 
                show={showForgotPassword} 
                onHide={() => setShowForgotPassword(false)}
            />
        </div>
    );
};

export default AuthPage;
