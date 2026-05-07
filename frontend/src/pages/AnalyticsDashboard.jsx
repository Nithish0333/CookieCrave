import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Badge, Alert, Spinner } from 'react-bootstrap';
import api from '../api';

const AnalyticsDashboard = () => {
    const [analyticsData, setAnalyticsData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchAnalyticsData();
    }, []);

    const fetchAnalyticsData = async () => {
        try {
            setLoading(true);
            const response = await api.get('/analytics/behaviors/analytics_summary/');
            setAnalyticsData(response.data);
        } catch (err) {
            setError('Failed to load analytics data');
            console.error('Analytics error:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '400px' }}>
                <div className="text-center">
                    <Spinner animation="border" variant="primary" />
                    <p className="mt-3">Loading analytics data...</p>
                </div>
            </Container>
        );
    }

    if (error) {
        return (
            <Container>
                <Alert variant="danger">{error}</Alert>
            </Container>
        );
    }

    if (!analyticsData) {
        return (
            <Container>
                <Alert variant="info">No analytics data available</Alert>
            </Container>
        );
    }

    const {
        total_sessions,
        total_page_views,
        total_product_views,
        total_searches,
        total_add_to_cart,
        total_purchases,
        avg_session_duration,
        popular_pages,
        popular_products,
        recent_searches
    } = analyticsData;

    return (
        <Container>
            <div className="dashboard-header mb-4">
                <h1 className="display-5 fw-bold mb-3">
                    <i className="bi bi-graph-up me-3"></i>
                    Analytics Dashboard
                </h1>
                <p className="lead text-muted">Real-time user behavior insights and metrics</p>
            </div>

            {/* Key Metrics */}
            <Row className="mb-4">
                <Col md={3}>
                    <Card className="metric-card h-100">
                        <Card.Body>
                            <div className="d-flex justify-content-between align-items-start">
                                <div>
                                    <h2 className="fw-bold text-primary">{total_sessions}</h2>
                                    <p className="text-muted mb-0">Total Sessions</p>
                                </div>
                                <i className="bi bi-people fs-1 text-muted opacity-25"></i>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
                
                <Col md={3}>
                    <Card className="metric-card h-100">
                        <Card.Body>
                            <div className="d-flex justify-content-between align-items-start">
                                <div>
                                    <h2 className="fw-bold text-info">{total_page_views}</h2>
                                    <p className="text-muted mb-0">Page Views</p>
                                </div>
                                <i className="bi bi-eye fs-1 text-muted opacity-25"></i>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
                
                <Col md={3}>
                    <Card className="metric-card h-100">
                        <Card.Body>
                            <div className="d-flex justify-content-between align-items-start">
                                <div>
                                    <h2 className="fw-bold text-warning">{total_product_views}</h2>
                                    <p className="text-muted mb-0">Product Views</p>
                                </div>
                                <i className="bi bi-cookie fs-1 text-muted opacity-25"></i>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
                
                <Col md={3}>
                    <Card className="metric-card h-100">
                        <Card.Body>
                            <div className="d-flex justify-content-between align-items-start">
                                <div>
                                    <h2 className="fw-bold text-success">{total_purchases}</h2>
                                    <p className="text-muted mb-0">Purchases</p>
                                </div>
                                <i className="bi bi-cart-check fs-1 text-muted opacity-25"></i>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            <Row>
                {/* Popular Pages */}
                <Col md={6}>
                    <Card className="mb-4">
                        <Card.Header>
                            <h5 className="mb-0">
                                <i className="bi bi-fire me-2"></i>
                                Popular Pages
                            </h5>
                        </Card.Header>
                        <Card.Body>
                            {popular_pages && popular_pages.length > 0 ? (
                                popular_pages.map((page, index) => (
                                    <div key={index} className="d-flex justify-content-between align-items-center py-2 border-bottom">
                                        <div>
                                            <strong>{page.page_title || 'Unknown Page'}</strong>
                                            <br />
                                            <small className="text-muted">{page.page_url?.substring(0, 50)}...</small>
                                        </div>
                                        <Badge bg="primary">{page.count} views</Badge>
                                    </div>
                                ))
                            ) : (
                                <p className="text-muted text-center py-4">No page view data available</p>
                            )}
                        </Card.Body>
                    </Card>
                </Col>

                {/* Popular Products */}
                <Col md={6}>
                    <Card className="mb-4">
                        <Card.Header>
                            <h5 className="mb-0">
                                <i className="bi bi-star me-2"></i>
                                Popular Products
                            </h5>
                        </Card.Header>
                        <Card.Body>
                            {popular_products && popular_products.length > 0 ? (
                                popular_products.map((product, index) => (
                                    <div key={index} className="d-flex justify-content-between align-items-center py-2 border-bottom">
                                        <div>
                                            <strong>{product.product__name || 'Unknown Product'}</strong>
                                            <br />
                                            <small className="text-muted">Viewed {product.count} times</small>
                                        </div>
                                        <Badge bg="warning">{product.count}</Badge>
                                    </div>
                                ))
                            ) : (
                                <p className="text-muted text-center py-4">No product view data available</p>
                            )}
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            <Row>
                {/* Recent Searches */}
                <Col md={6}>
                    <Card className="mb-4">
                        <Card.Header>
                            <h5 className="mb-0">
                                <i className="bi bi-search me-2"></i>
                                Recent Search Terms
                            </h5>
                        </Card.Header>
                        <Card.Body>
                            {recent_searches && recent_searches.length > 0 ? (
                                recent_searches.map((search, index) => (
                                    <div key={index} className="d-flex justify-content-between align-items-center py-2 border-bottom">
                                        <div>
                                            <i className="bi bi-search me-2 text-muted"></i>
                                            <strong>{search.search_query}</strong>
                                        </div>
                                        <Badge bg="info">{search.count} searches</Badge>
                                    </div>
                                ))
                            ) : (
                                <p className="text-muted text-center py-4">No search data available</p>
                            )}
                        </Card.Body>
                    </Card>
                </Col>

                {/* Engagement Metrics */}
                <Col md={6}>
                    <Card className="mb-4">
                        <Card.Header>
                            <h5 className="mb-0">
                                <i className="bi bi-graph-up me-2"></i>
                                Engagement Metrics
                            </h5>
                        </Card.Header>
                        <Card.Body>
                            <Row>
                                <Col md={6} className="text-center mb-3">
                                    <h4 className="text-primary">{(avg_session_duration || 0).toFixed(1)}s</h4>
                                    <p className="text-muted mb-0">Avg Session Duration</p>
                                </Col>
                                <Col md={6} className="text-center mb-3">
                                    <h4 className="text-info">{total_searches}</h4>
                                    <p className="text-muted mb-0">Total Searches</p>
                                </Col>
                                <Col md={6} className="text-center mb-3">
                                    <h4 className="text-warning">{total_add_to_cart}</h4>
                                    <p className="text-muted mb-0">Add to Cart Actions</p>
                                </Col>
                                <Col md={6} className="text-center mb-3">
                                    <h4 className="text-success">
                                        {total_page_views > 0 ? ((total_add_to_cart / total_page_views) * 100).toFixed(1) : 0}%
                                    </h4>
                                    <p className="text-muted mb-0">Cart Conversion Rate</p>
                                </Col>
                            </Row>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

export default AnalyticsDashboard;
