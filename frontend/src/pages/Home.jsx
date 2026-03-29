import React, { useState, useEffect, useMemo } from 'react';
import { Container, Card, Button, ListGroup, Badge, Form, Row, Col } from 'react-bootstrap';
import { useSearchParams } from 'react-router-dom';
import api, { recommendationAPI } from '../api';
import { useCart } from '../CartContext';
import analytics from '../services/analyticsService';
import RecommendationCarousel from '../components/RecommendationCarousel';
import WishlistButton from '../components/WishlistButton';
import { getProductImageUrl, getPlaceholderImageUrl } from '../utils/imageUtils';

const SORT_OPTIONS = [
  { value: 'price_asc', label: 'Price: Low to High' },
  { value: 'price_desc', label: 'Price: High to Low' },
  { value: 'name_asc', label: 'Name: A to Z' },
  { value: 'name_desc', label: 'Name: Z to A' },
  { value: 'newest', label: 'Newest first' },
];

const Home = () => {
    const [searchParams] = useSearchParams();
    const urlQuery = searchParams.get('q') || '';
    const selectedProductId = searchParams.get('product') || '';
    const [products, setProducts] = useState([]);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [searchQuery, setSearchQuery] = useState(urlQuery);
    const [sortBy, setSortBy] = useState('price_asc');
    const [minPrice, setMinPrice] = useState('');
    const [maxPrice, setMaxPrice] = useState('');
    const [inStockOnly, setInStockOnly] = useState(false);
    const [sugarFree, setSugarFree] = useState(false);
    const [glutenFree, setGlutenFree] = useState(false);
    const [recommendations, setRecommendations] = useState({
        hybrid: [],
        trending: [],
    });
    const [loadingRecs, setLoadingRecs] = useState({
        hybrid: false,
        trending: false,
    });
    const [errorRecs, setErrorRecs] = useState({
        hybrid: null,
        trending: null,
    });
    const { addToCart } = useCart();

    useEffect(() => {
        analytics.trackHomePageView();
        fetchRecommendations('hybrid');
        fetchRecommendations('trending');
    }, []);

    useEffect(() => {
        setSearchQuery(urlQuery);
        // Auto-select "All Cookies" when there's a search query or selected product
        if (urlQuery.trim() || selectedProductId) {
            setSelectedCategory(null);
        }
    }, [urlQuery, selectedProductId]);

    useEffect(() => {
        fetchCategories();
        fetchProducts();
    }, []);

    const fetchRecommendations = async (algorithm) => {
        setLoadingRecs((prev) => ({ ...prev, [algorithm]: true }));
        setErrorRecs((prev) => ({ ...prev, [algorithm]: null }));

        try {
            const response = await recommendationAPI.getRecommendations(algorithm, 8);
            setRecommendations((prev) => ({
                ...prev,
                [algorithm]: response.data.recommendations || [],
            }));

            analytics.track('recommendations_viewed_home', {
                algorithm,
                quantity: response.data.recommendations?.length || 0,
            });
        } catch (error) {
            console.error(`Error fetching ${algorithm} recommendations:`, error);
            setErrorRecs((prev) => ({
                ...prev,
                [algorithm]: null, // Don't show error message on home page
            }));
        } finally {
            setLoadingRecs((prev) => ({ ...prev, [algorithm]: false }));
        }
    };

    const fetchCategories = async () => {
        try {
            const res = await api.get('categories/');
            setCategories(res.data);
        } catch (err) {
            console.error('Error fetching categories:', err);
        }
    };

    const fetchProducts = async () => {
        try {
            const res = await api.get('products/');
            setProducts(res.data);
        } catch (err) {
            console.error('Error fetching products:', err);
        }
    };

    const handleAddToCart = (product) => {
        // Track add to cart event
        analytics.track('add_to_cart', {
            product_id: product.id,
            product_name: product.name,
            product_price: product.price,
            product_category: product.category_name,
            stock_available: product.stock,
            source: 'product_grid'
        });
        
        addToCart(product, 1);
    };

    const filteredProducts = useMemo(() => {
        let list = products;

        if (selectedCategory) {
            list = list.filter(p => Number(p.category) === Number(selectedCategory));
        }
        if (selectedProductId) {
            list = list.filter(p => Number(p.id) === Number(selectedProductId));
        }
        if (searchQuery.trim()) {
            const q = searchQuery.toLowerCase();
            list = list.filter(p => {
                const name = (p.name || '').toLowerCase();
                const desc = (p.description || '').toLowerCase();
                const cat = (p.category_name || '').toLowerCase();
                return name.includes(q) || desc.includes(q) || cat.includes(q);
            });
        }
        const min = minPrice !== '' ? parseFloat(minPrice) : null;
        const max = maxPrice !== '' ? parseFloat(maxPrice) : null;
        if (min != null && !isNaN(min)) {
            list = list.filter(p => Number(p.price) >= min);
        }
        if (max != null && !isNaN(max)) {
            list = list.filter(p => Number(p.price) <= max);
        }
        if (inStockOnly) {
            list = list.filter(p => (p.stock ?? 0) > 0);
        }
        if (sugarFree) {
            const match = (s) => /sugar[- ]?free/i.test(s || '');
            list = list.filter(p => match(p.name) || match(p.description));
        }
        if (glutenFree) {
            const match = (s) => /gluten[- ]?free/i.test(s || '');
            list = list.filter(p => match(p.name) || match(p.description));
        }

        const sorted = [...list];
        switch (sortBy) {
            case 'price_asc':
                sorted.sort((a, b) => Number(a.price) - Number(b.price));
                break;
            case 'price_desc':
                sorted.sort((a, b) => Number(b.price) - Number(a.price));
                break;
            case 'name_asc':
                sorted.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
                break;
            case 'name_desc':
                sorted.sort((a, b) => (b.name || '').localeCompare(a.name || ''));
                break;
            case 'newest':
                sorted.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
                break;
            default:
                break;
        }
        return sorted;
    }, [products, selectedCategory, selectedProductId, searchQuery, minPrice, maxPrice, inStockOnly, sugarFree, glutenFree, sortBy]);

    return (
        <div>
            <div className="hero-section">
                <Container className="d-flex align-items-center">
                    <img src="/logo.png" alt="CookieCrave Logo" style={{ width: '100px', marginRight: '30px' }} className="hero-logo-animate" />
                    <div>
                        <h1 className="display-4 fw-bold mb-4 text-warning">Welcome to CookieCrave</h1>
                        <p className="lead mb-0 text-light">The premium marketplace for buying and selling homemade cookies.</p>
                    </div>
                </Container>
            </div>

            {/* Recommendation Carousels */}
            {recommendations.hybrid.length > 0 && (
                <RecommendationCarousel
                    items={recommendations.hybrid}
                    title="✨ Recommended For You"
                    algorithm="hybrid"
                    isLoading={loadingRecs.hybrid}
                    error={errorRecs.hybrid}
                />
            )}

            {recommendations.trending.length > 0 && (
                <RecommendationCarousel
                    items={recommendations.trending}
                    title="🔥 Trending This Month"
                    algorithm="trending"
                    isLoading={loadingRecs.trending}
                    error={errorRecs.trending}
                />
            )}
            
            <div style={{ display: 'flex', minHeight: 'calc(100vh - 200px)' }}>
                {/* Static Categories Sidebar */}
                <div style={{
                    width: '25%',
                    backgroundColor: '#fff',
                    padding: '20px',
                    boxShadow: '2px 0 8px rgba(0,0,0,0.1)',
                    overflowY: 'auto',
                    maxHeight: 'calc(100vh - 200px)',
                    borderRight: '1px solid #e9ecef'
                }}>
                    <h4 className="mb-3 fw-bold" style={{
                        fontSize: '1.3rem',
                        color: '#2c3e50',
                        paddingBottom: '10px',
                        borderBottom: '3px solid #ffc107'
                    }}>🍪 Categories</h4>
                    <ListGroup className="category-menu" style={{
                        borderRadius: '12px',
                        overflow: 'hidden',
                        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                    }}>
                        <ListGroup.Item 
                            className={`d-flex align-items-center ${!selectedCategory ? 'active' : ''}`}
                            onClick={() => setSelectedCategory(null)}
                            style={{
                                cursor: 'pointer',
                                padding: '12px 16px',
                                transition: 'all 0.3s ease',
                                backgroundColor: !selectedCategory ? '#ffc107' : '#fff',
                                color: !selectedCategory ? '#fff' : '#333',
                                fontWeight: !selectedCategory ? 'bold' : 'normal',
                                borderLeft: !selectedCategory ? '4px solid #ff9800' : 'none',
                                border: 'none'
                            }}
                            onMouseEnter={(e) => {
                                if (selectedCategory !== null) {
                                    e.currentTarget.style.backgroundColor = '#f8f9fa';
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (selectedCategory !== null) {
                                    e.currentTarget.style.backgroundColor = '#fff';
                                }
                            }}
                        >
                            <span className="me-2" style={{ fontSize: '1.2rem' }}>🍪</span>
                            <span>All Cookies</span>
                        </ListGroup.Item>
                        {categories.map(c => (
                            <ListGroup.Item 
                                key={c.id}
                                className={`d-flex align-items-center ${selectedCategory === c.id ? 'active' : ''}`}
                                onClick={() => setSelectedCategory(c.id)}
                                style={{
                                    cursor: 'pointer',
                                    padding: '12px 16px',
                                    transition: 'all 0.3s ease',
                                    backgroundColor: selectedCategory === c.id ? '#ffc107' : '#fff',
                                    color: selectedCategory === c.id ? '#fff' : '#333',
                                    fontWeight: selectedCategory === c.id ? 'bold' : 'normal',
                                    borderLeft: selectedCategory === c.id ? '4px solid #ff9800' : 'none',
                                    border: 'none'
                                }}
                                onMouseEnter={(e) => {
                                    if (selectedCategory !== c.id) {
                                        e.currentTarget.style.backgroundColor = '#f8f9fa';
                                    }
                                }}
                                onMouseLeave={(e) => {
                                    if (selectedCategory !== c.id) {
                                        e.currentTarget.style.backgroundColor = '#fff';
                                    }
                                }}
                            >
                                {c.image || c.image_url ? (
                                    <img 
                                        src={getProductImageUrl(c.image || c.image_url, getPlaceholderImageUrl(c.name, 40, 40))} 
                                        alt={c.name} 
                                        style={{ width: 40, height: 40, objectFit: 'cover', borderRadius: 6, marginRight: 12 }}
                                        crossOrigin="anonymous"
                                        onError={(e) => {
                                            e.target.onerror = null;
                                            e.target.src = getPlaceholderImageUrl(c.name, 40, 40);
                                        }}
                                    />
                                ) : (
                                    <div style={{ 
                                        width: 40, 
                                        height: 40, 
                                        borderRadius: 6, 
                                        backgroundColor: '#f8f9fa', 
                                        display: 'flex', 
                                        alignItems: 'center', 
                                        justifyContent: 'center', 
                                        marginRight: 12 
                                    }}>
                                        🍪
                                    </div>
                                )}
                                <span>{c.name}</span>
                            </ListGroup.Item>
                        ))}
                    </ListGroup>
                </div>

                {/* Main Content Area */}
                <div style={{
                    width: '75%',
                    padding: '20px',
                    overflowY: 'auto',
                    maxHeight: 'calc(100vh - 200px)'
                }}>
                    <div style={{
                        backgroundColor: '#f8f9fa',
                        borderRadius: '12px',
                        padding: '20px',
                        marginBottom: '30px',
                        border: '1px solid #e9ecef',
                        boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
                    }}>
                        <div className="d-flex flex-wrap align-items-center gap-4">
                            {/* Price Range Section */}
                            <div>
                                <label className="fw-bold mb-2 d-block" style={{ fontSize: '0.9rem', color: '#495057' }}>💰 Price Range</label>
                                <div className="d-flex align-items-center gap-2">
                                    <Form.Control
                                        type="number"
                                        placeholder="Min ₹"
                                        min={0}
                                        step={10}
                                        value={minPrice}
                                        onChange={(e) => setMinPrice(e.target.value)}
                                        size="sm"
                                        style={{ width: 90, borderRadius: '6px' }}
                                    />
                                    <span className="text-muted fw-bold">–</span>
                                    <Form.Control
                                        type="number"
                                        placeholder="Max ₹"
                                        min={0}
                                        step={10}
                                        value={maxPrice}
                                        onChange={(e) => setMaxPrice(e.target.value)}
                                        size="sm"
                                        style={{ width: 90, borderRadius: '6px' }}
                                    />
                                </div>
                            </div>

                            {/* Dietary Filters Section */}
                            <div>
                                <label className="fw-bold mb-2 d-block" style={{ fontSize: '0.9rem', color: '#495057' }}>🥗 Dietary</label>
                                <Form.Select
                                    value={`${inStockOnly}-${sugarFree}-${glutenFree}`}
                                    onChange={(e) => {
                                        const [stock, sugar, gluten] = e.target.value.split('-').map(v => v === 'true');
                                        setInStockOnly(stock);
                                        setSugarFree(sugar);
                                        setGlutenFree(gluten);
                                    }}
                                    size="sm"
                                    style={{ width: 'auto', minWidth: 180, borderRadius: '6px' }}
                                >
                                    <option value="false-false-false">All items</option>
                                    <option value="true-false-false">✓ In stock only</option>
                                    <option value="false-true-false">🍬 Sugar free</option>
                                    <option value="false-false-true">🌾 Gluten free</option>
                                    <option value="true-true-false">✓ In stock + 🍬 Sugar free</option>
                                    <option value="true-false-true">✓ In stock + 🌾 Gluten free</option>
                                    <option value="false-true-true">🍬 Sugar free + 🌾 Gluten free</option>
                                    <option value="true-true-true">✓ All filters</option>
                                </Form.Select>
                            </div>

                            {/* Sort Section */}
                            <div>
                                <label className="fw-bold mb-2 d-block" style={{ fontSize: '0.9rem', color: '#495057' }}>📊 Sort By</label>
                                <Form.Select
                                    value={sortBy}
                                    onChange={(e) => setSortBy(e.target.value)}
                                    size="sm"
                                    style={{ width: 'auto', minWidth: 180, borderRadius: '6px' }}
                                >
                                    {SORT_OPTIONS.map(opt => (
                                        <option key={opt.value} value={opt.value}>{opt.label}</option>
                                    ))}
                                </Form.Select>
                            </div>

                            {/* Active Filters Display */}
                            {(minPrice || maxPrice || inStockOnly || sugarFree || glutenFree) && (
                                <div style={{ marginLeft: 'auto' }}>
                                    <div className="d-flex gap-2 flex-wrap">
                                        {minPrice && (
                                            <Badge bg="info" style={{ padding: '6px 12px', fontSize: '0.85rem' }}>
                                                Min: ₹{minPrice}
                                            </Badge>
                                        )}
                                        {maxPrice && (
                                            <Badge bg="info" style={{ padding: '6px 12px', fontSize: '0.85rem' }}>
                                                Max: ₹{maxPrice}
                                            </Badge>
                                        )}
                                        {inStockOnly && (
                                            <Badge bg="success" style={{ padding: '6px 12px', fontSize: '0.85rem' }}>
                                                ✓ In Stock
                                            </Badge>
                                        )}
                                        {sugarFree && (
                                            <Badge bg="warning" style={{ padding: '6px 12px', fontSize: '0.85rem' }}>
                                                🍬 Sugar Free
                                            </Badge>
                                        )}
                                        {glutenFree && (
                                            <Badge bg="danger" style={{ padding: '6px 12px', fontSize: '0.85rem' }}>
                                                🌾 Gluten Free
                                            </Badge>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                    <h4 className="mb-3 fw-bold">Delicious Treats</h4>
                    <Row>
                        {filteredProducts.map(p => (
                            <Col md={4} key={p.id} className="mb-4">
                                <Card 
                                    data-product-id={p.id}
                                    className="product-card"
                                    onClick={() => {
                                        analytics.trackProductView(p.id, {
                                            source: 'product_grid',
                                            category: p.category_name,
                                            price: p.price,
                                            position: filteredProducts.findIndex(product => product.id === p.id) + 1
                                        });
                                    }}
                                >
                                    <div style={{ height: '200px', backgroundColor: '#f8f9fa', overflow: 'hidden' }}>
                                        <img 
                                            src={getProductImageUrl(p.image, getPlaceholderImageUrl(p.name))}
                                            alt={p.name} 
                                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                                            crossOrigin="anonymous"
                                            onError={(e) => {
                                                e.target.onerror = null;
                                                e.target.src = getPlaceholderImageUrl(p.name);
                                            }}
                                        />
                                    </div>
                                    <Card.Body>
                                        <Card.Title className="fw-bold">{p.name}</Card.Title>
                                        <Badge bg="secondary" className="mb-2">{p.category_name}</Badge>
                                        <Card.Text className="text-muted small" style={{ height: '40px', overflow: 'hidden' }}>
                                            {p.description}
                                        </Card.Text>
                                        <div className="d-flex justify-content-between align-items-center mt-3">
                                            <h5 className="mb-0 fw-bold text-danger">₹{p.price}</h5>
                                            <div className="d-flex gap-2">
                                                <WishlistButton 
                                                    productId={p.id} 
                                                    productName={p.name}
                                                    className="btn-sm"
                                                />
                                                <Button 
                                                    variant="primary" 
                                                    size="sm" 
                                                    onClick={(e) => {
                                                        e.stopPropagation(); // Prevent card click
                                                        handleAddToCart(p);
                                                    }}
                                                    data-track="add-to-cart"
                                                    data-product-id={p.id}
                                                    data-product-name={p.name}
                                                >Add to Cart</Button>
                                            </div>
                                        </div>
                                    </Card.Body>
                                </Card>
                            </Col>
                        ))}
                        {filteredProducts.length === 0 && (
                            <Col><p className="text-muted">
                                {searchQuery ? `No results for "${searchQuery}".` : 'No cookies found in this category.'}
                            </p></Col>
                        )}
                    </Row>
                </div>
            </div>
        </div>
    );
};

export default Home;
