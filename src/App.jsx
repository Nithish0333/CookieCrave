import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { Navbar, Nav, Container, NavDropdown, Badge } from 'react-bootstrap';
import api from './api';
// Import analytics safely
let analytics;
try {
  analytics = require('./services/analyticsService').default;
} catch (err) {
  console.warn('Analytics not available');
  analytics = {
    track: () => {},
    trackPageView: () => {},
    getTimeOnPage: () => 0,
    identify: () => {}
  };
}
import Home from './pages/Home';
import AuthPage from './pages/AuthPage';
import Dashboard from './pages/Dashboard';
import CartPage from './pages/CartPage';
import WishlistPage from './pages/WishlistPage';
import AboutPage from './pages/AboutPage';
import CustomerSupportPage from './pages/CustomerSupportPage';
import ContactPage from './pages/ContactPage';
import GiftingCookiesPage from './pages/GiftingCookiesPage';
import DiscountGamesPage from './pages/DiscountGamesPage';
import WholesalePage from './pages/WholesalePage';
import ChatbotPage from './pages/ChatbotPage';
import AnalyticsDashboard from './pages/AnalyticsDashboard';
import RecommendationsPage from './pages/RecommendationsPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import SimpleLogin from './components/SimpleLogin';
import { CartProvider, useCart } from './CartContext';
import NavSearchBar from './components/NavSearchBar';

const ProtectedRoute = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem('access') || !!sessionStorage.getItem('access');
  return isAuthenticated ? children : <Navigate to="/login" />;
};

const Navigation = ({ mode, toggleMode, username }) => {
  const location = useLocation();
  const isAuthPage = location.pathname === '/' || location.pathname === '/login' || location.pathname === '/signup' || location.pathname.startsWith('/reset-password');
  const isAuthenticated = !!localStorage.getItem('access') || !!sessionStorage.getItem('access');
  const { itemCount } = useCart();
  
  if (isAuthPage) return null;

  const logout = () => {
    // Track logout event
    analytics.track('user_logout', {
      session_duration: analytics.getTimeOnPage(),
      last_page: window.location.pathname
    });
    
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    sessionStorage.removeItem('access');
    sessionStorage.removeItem('refresh');
    window.location.href = '/login';
  };

  // Generate a color based on username
  const getAvatarColor = (name) => {
    const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'];
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
  };

  const avatarColor = getAvatarColor(username);
  const initials = username ? username.charAt(0).toUpperCase() : 'U';

  return (
      <Navbar bg="dark" variant="dark" expand="lg" sticky="top" className="shadow-sm">
        <Container fluid className="ps-0 pe-0">
          <Navbar.Brand as={Link} to="/" className="brand-animate" style={{ marginLeft: '0rem' }}>
            <img src="/logo.png" alt="CookieCrave Logo" style={{ width: '28px', height: '28px', marginRight: '4px' }} />
            <span className="d-none d-md-inline">CookieCrave</span>
            <span className="d-md-none">CC</span>
          </Navbar.Brand>
          
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              {mode === 'buy' ? (
                <React.Fragment>
                  <Nav.Link as={Link} to="/home" data-track="navigation" data-page="marketplace">Marketplace</Nav.Link>
                  {isAuthenticated && <Nav.Link as={Link} to="/recommendations" data-track="navigation" data-page="recommendations">Recommendations</Nav.Link>}
                  {isAuthenticated && <Nav.Link as={Link} to="/dashboard" data-track="navigation" data-page="my_purchases">Purchases</Nav.Link>}
                  <Nav.Link as={Link} to="/about" data-track="navigation" data-page="about">About</Nav.Link>
                  <Nav.Link as={Link} to="/contact" data-track="navigation" data-page="contact">Contact</Nav.Link>
                  {isAuthenticated && (
                    <Nav.Link as={Link} to="/assistant" data-track="navigation" data-page="assistant">
                      Assistant
                    </Nav.Link>
                  )}
                </React.Fragment>
              ) : (
                <React.Fragment>
                  {isAuthenticated && <Nav.Link as={Link} to="/dashboard" data-track="navigation" data-page="selling_dashboard">Dashboard</Nav.Link>}
                  <Nav.Link as={Link} to="/about" data-track="navigation" data-page="about">About</Nav.Link>
                  <Nav.Link as={Link} to="/contact" data-track="navigation" data-page="contact">Contact</Nav.Link>
                  {isAuthenticated && (
                    <Nav.Link as={Link} to="/assistant" data-track="navigation" data-page="assistant">
                      Assistant
                    </Nav.Link>
                  )}
                </React.Fragment>
              )}
            </Nav>
            
            <Nav className="ms-auto">
              {isAuthenticated && mode === 'buy' && (
                <div className="px-1">
                  <NavSearchBar />
                </div>
              )}
              
              {isAuthenticated && (
                <>
                  <Nav.Link as={Link} to="/wishlist" className="position-relative" data-track="navigation" data-page="wishlist">
                    <i className="bi bi-heart" style={{ fontSize: '1rem' }}></i>
                    <span className="ms-1 d-none d-xl-inline">Wishlist</span>
                  </Nav.Link>
                  
                  <Nav.Link as={Link} to="/cart" className="position-relative" data-track="navigation" data-page="cart">
                    <i className="bi bi-cart3" style={{ fontSize: '1rem' }}></i>
                    <span className="ms-1 d-none d-xl-inline">Cart</span>
                    {itemCount > 0 && (
                      <Badge bg="danger" className="position-absolute" style={{ top: '-4px', right: '-4px', fontSize: '0.6rem', padding: '2px 4px' }}>
                        {itemCount}
                      </Badge>
                    )}
                  </Nav.Link>
                </>
              )}
              
              {isAuthenticated && (
                <div 
                  className="mode-toggle-switch me-2"
                  onClick={toggleMode}
                  title={`Switch to ${mode === 'buy' ? 'Selling' : 'Buying'} Mode`}
                  role="switch"
                  aria-checked={mode === 'buy'}
                >
                  <div className={`toggle-container ${mode === 'buy' ? 'buy-mode' : 'sell-mode'}`}>
                    <div className="toggle-track"></div>
                    <div className="toggle-thumb">
                      <span className="toggle-icon">{mode === 'buy' ? '🛒' : '💰'}</span>
                    </div>
                    <div className="toggle-labels">
                      <span className="label buy-label">Buy</span>
                      <span className="label sell-label">Sell</span>
                    </div>
                  </div>
                </div>
              )}
              
              {isAuthenticated ? (
                <>
                  <NavDropdown 
                    title={
                      <span style={{ color: '#fff' }}>
                        <div
                          style={{
                            width: '28px',
                            height: '28px',
                            borderRadius: '50%',
                            backgroundColor: avatarColor,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: '#fff',
                            fontWeight: 'bold',
                            fontSize: '11px',
                            marginRight: '6px'
                          }}
                        >
                          {initials}
                        </div>
                        <span className="d-none d-xxl-inline">{username || 'Account'}</span>
                      </span>
                    } 
                    id="user-nav-dropdown"
                    align="end"
                    className="custom-profile-dropdown"
                  >
                    <NavDropdown.Item as={Link} to="/dashboard">
                      <i className="bi bi-speedometer2 me-2"></i> Dashboard
                    </NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item onClick={logout} className="text-danger">
                      <i className="bi bi-box-arrow-right me-2"></i> Logout
                    </NavDropdown.Item>
                  </NavDropdown>
                </>
              ) : (
                <div className="d-flex align-items-center gap-1 flex-shrink-0">
                  <Nav.Link as={Link} to="/login" className="btn btn-outline-light btn-sm px-2 py-1">Login</Nav.Link>
                  <Nav.Link as={Link} to="/signup" className="btn btn-light btn-sm px-2 py-1">Signup</Nav.Link>
                </div>
              )}
              <NavDropdown
                title={<i className="bi bi-three-dots-vertical" style={{ fontSize: '1rem', color: '#fff' }}></i>}
                id="more-nav-dropdown"
                align="end"
                className="ms-1"
              >
                <NavDropdown.Item as={Link} to="/gifting-cookies" data-track="navigation" data-page="gifting_cookies">
                  <i className="bi bi-gift me-2"></i> Gifting Cookies
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/discount-games" data-track="navigation" data-page="discount_games">
                  <i className="bi bi-dice-5 me-2"></i> Discount Games
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/wholesale" data-track="navigation" data-page="wholesale_bulk_orders">
                  <i className="bi bi-boxes me-2"></i> Wholesale & Bulk Orders
                </NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/customer-support" data-track="navigation" data-page="customer_support">
                  <i className="bi bi-headset me-2"></i> Customer Support
                </NavDropdown.Item>
                {isAuthenticated && (
                  <React.Fragment>
                    <NavDropdown.Divider />
                    <NavDropdown.Item as={Link} to="/analytics" data-track="navigation" data-page="analytics">
                      <i className="bi bi-graph-up me-2"></i> Analytics
                    </NavDropdown.Item>
                  </React.Fragment>
                )}
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
  );
};

function AppContent() {
  const [mode, setMode] = React.useState('buy');
  const [username, setUsername] = React.useState('');
  const isAuthenticated = !!localStorage.getItem('access') || !!sessionStorage.getItem('access');
  const navigate = useNavigate();
  const location = useLocation();

  // Track page views on route changes
  React.useEffect(() => {
    analytics.trackPageView();
    
    // Track mode changes
    analytics.track('mode_change', {
      mode: mode,
      page: location.pathname
    });
  }, [location.pathname, mode]);

  React.useEffect(() => {
    if (isAuthenticated) {
      fetchProfile();
    }
  }, [isAuthenticated]);

  const fetchProfile = async () => {
    try {
      const res = await api.get('users/profile/');
      setUsername(res.data.username);
      
      // Track user identification
      analytics.identify(res.data.username, {
        email: res.data.email,
        user_id: res.data.id
      });
      
      analytics.track('user_login', {
          username: res.data.username
      });
      

    } catch (err) {
      console.error('Error fetching profile', err);
    }
  };

  const toggleMode = () => {
    setMode(prev => {
      const next = prev === 'buy' ? 'sell' : 'buy';
      
      // Track mode toggle
      analytics.track('mode_toggle', {
        from_mode: prev,
        to_mode: next,
        current_page: location.pathname
      });
      
      if (next === 'buy') {
        navigate('/home');
      } else {
        navigate('/dashboard');
      }
      return next;
    });
  };

  return (
    <>
      <Navigation mode={mode} toggleMode={toggleMode} username={username} />
      <Container className={['/', '/login', '/signup'].includes(window.location.pathname) || window.location.pathname.startsWith('/reset-password') ? "mt-4 d-flex justify-content-center" : "mt-4"}>
        <Routes>
          <Route path="/" element={isAuthenticated ? <Navigate to="/home" replace /> : <AuthPage />} />
          <Route path="/login" element={isAuthenticated ? <Navigate to="/home" replace /> : <AuthPage />} />
          <Route path="/signup" element={isAuthenticated ? <Navigate to="/home" replace /> : <AuthPage />} />
          <Route path="/reset-password/:uidb64/:token" element={<ResetPasswordPage />} />
          <Route path="/simple-login" element={<SimpleLogin />} />
          <Route path="/home" element={
            <ProtectedRoute>
              {mode === 'buy' ? <Home /> : <Navigate to="/dashboard" replace />}
            </ProtectedRoute>
          } />
          <Route path="/recommendations" element={
            <ProtectedRoute>
              {mode === 'buy' ? <RecommendationsPage /> : <Navigate to="/dashboard" replace />}
            </ProtectedRoute>
          } />
          <Route path="/cart" element={
            <ProtectedRoute>
              <CartPage />
            </ProtectedRoute>
          } />
          <Route path="/wishlist" element={
            <ProtectedRoute>
              <WishlistPage />
            </ProtectedRoute>
          } />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard globalMode={mode} currentUser={username} /></ProtectedRoute>} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/customer-support" element={<CustomerSupportPage />} />
          <Route path="/gifting-cookies" element={<ProtectedRoute><GiftingCookiesPage /></ProtectedRoute>} />
          <Route path="/discount-games" element={<ProtectedRoute><DiscountGamesPage /></ProtectedRoute>} />
          <Route path="/wholesale" element={<ProtectedRoute><WholesalePage /></ProtectedRoute>} />
          <Route path="/analytics" element={<ProtectedRoute><AnalyticsDashboard /></ProtectedRoute>} />
          <Route path="/assistant" element={<ProtectedRoute><ChatbotPage /></ProtectedRoute>} />
        </Routes>
      </Container>
    </>
  );
}

function App() {
  return (
    <CartProvider>
      <Router>
        <AppContent />
      </Router>
    </CartProvider>
  );
}

export default App;
