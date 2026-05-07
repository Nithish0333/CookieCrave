import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Form, Button, Table, Badge } from 'react-bootstrap';
import api from '../api';
import analytics from '../services/analyticsService';
import SellerRegisterModal from '../components/SellerRegisterModal';
import { getProductImageUrl, getPlaceholderImageUrl } from '../utils/imageUtils';

const Dashboard = ({ globalMode, currentUser }) => {
    const mode = globalMode;
    const [transactions, setTransactions] = useState([]);
    const [myProducts, setMyProducts] = useState([]);
    
    // Seller registration states
    const [isSeller, setIsSeller] = useState(false);
    const [checkingSeller, setCheckingSeller] = useState(true);
    const [showSellerModal, setShowSellerModal] = useState(false);
    
    // Selling states
    const [categories, setCategories] = useState([]);
    const [productName, setProductName] = useState('');
    const [productDesc, setProductDesc] = useState('');
    const [productPrice, setProductPrice] = useState('');
    const [productCat, setProductCat] = useState('');
    const [productStock, setProductStock] = useState('10');
    const [productImage, setProductImage] = useState(null);

    useEffect(() => {
        analytics.trackSellingPageView();
        fetchTransactions();
        fetchCategories();
        if (mode === 'sell') {
            checkSellerStatus();
            fetchMyProducts();
        }
    }, [mode]);

    const checkSellerStatus = async () => {
        try {
            setCheckingSeller(true);
            const res = await api.get('users/profile/');
            setIsSeller(res.data.is_seller);
        } catch (err) {
            console.error('Error checking seller status');
        } finally {
            setCheckingSeller(false);
        }
    };

    const fetchMyProducts = async () => {
        try {
            const res = await api.get('products/?user_only=true');
            setMyProducts(res.data);
        } catch (err) {
            console.error('Error fetching my products');
        }
    };

    const fetchTransactions = async () => {
        try {
            const res = await api.get('transactions/');
            setTransactions(res.data);
        } catch (err) {
            console.error('Error fetching transactions');
        }
    };

    const handleRegistrationSuccess = () => {
        checkSellerStatus();
    };

    const fetchCategories = async () => {
        try {
            const res = await api.get('categories/');
            setCategories(res.data);
            if (res.data.length > 0) setProductCat(res.data[0].id);
        } catch (err) {
            console.error('Error fetching categories');
        }
    };

    const handleCreateProduct = async (e) => {
        e.preventDefault();
        try {
            const formData = new FormData();
            formData.append('name', productName);
            formData.append('description', productDesc);
            formData.append('price', productPrice);
            formData.append('category', productCat);
            formData.append('stock', productStock);
            if (productImage) {
                formData.append('image', productImage);
            }

            await api.post('products/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert('Cookie listed successfully!');
            fetchMyProducts();
            setProductName('');
            setProductDesc('');
            setProductPrice('');
            setProductStock('10');
            setProductImage(null);
        } catch (err) {
            console.error('Error creating product', err);
            alert('Failed to list cookie. Please check all fields.');
        }
    };

    const handleDeleteProduct = async (id) => {
        if (window.confirm('Are you sure you want to delete this listing?')) {
            try {
                await api.delete(`products/${id}/`);
                fetchMyProducts();
            } catch (err) {
                console.error('Error deleting product', err);
            }
        }
    };

    const mySales = transactions.filter(t => t.product_detail?.seller_username === currentUser);
    const totalEarnings = mySales.reduce((sum, t) => sum + parseFloat(t.total_price), 0).toFixed(2);

    return (
        <>
            <style>{`
                .card:hover {
                    transform: none !important;
                    box-shadow: 0 8px 24px rgba(0,0,0,0.04) !important;
                }
            `}</style>
            <div>
                <h2 className="fw-bold mb-4 text-center">Your Dashboard</h2>
            

            {mode === 'buy' ? (
                <Card className="p-4 shadow-sm">
                    <h4 className="mb-4 fw-bold text-success">
                        <i className="bi bi-cart-check me-2"></i> My Purchases
                    </h4>
                    <Table responsive hover>
                        <thead className="table-light">
                            <tr>
                                <th>Order ID</th>
                                <th>Cookie</th>
                                <th>Quantity</th>
                                <th>Total Price</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {transactions.filter(t => t.user_username === currentUser).map(t => (
                                <tr key={t.id}>
                                    <td>#{t.id}</td>
                                    <td>{t.product_detail?.name}</td>
                                    <td>{t.quantity}</td>
                                    <td className="fw-bold text-success">₹{t.total_price}</td>
                                    <td><Badge bg="success">{t.status}</Badge></td>
                                    <td>{new Date(t.created_at).toLocaleDateString()}</td>
                                </tr>
                            ))}
                            {transactions.filter(t => t.user_username === currentUser).length === 0 && (
                                <tr>
                                    <td colSpan="6" className="text-center text-muted py-4">No purchases yet. Start craving!</td>
                                </tr>
                            )}
                        </tbody>
                    </Table>
                </Card>
            ) : (
                <>
                {checkingSeller ? (
                    <div className="text-center py-5">
                        <div className="spinner-border text-danger" role="status"></div>
                        <div className="mt-2 text-muted">Checking seller profile...</div>
                    </div>
                ) : !isSeller ? (
                    <div className="d-flex justify-content-center">
                        <Card className="p-0 shadow-sm mb-4 border-0 w-100 overflow-hidden" style={{ maxWidth: '800px', borderRadius: '15px' }}>
                            <Row className="g-0">
                                <Col md={6} className="d-none d-md-block">
                                    <div className="h-100" style={{
                                        backgroundImage: 'url(/seller_onboarding_illustration.png)',
                                        backgroundSize: 'cover',
                                        backgroundPosition: 'center',
                                        minHeight: '400px'
                                    }}></div>
                                </Col>
                                <Col md={6}>
                                    <div className="p-5 d-flex flex-column justify-content-center h-100">
                                        <Badge bg="danger" className="mb-3 align-self-start py-2 px-3" style={{borderRadius: '20px'}}>Free Registration</Badge>
                                        <h2 className="fw-bold mb-3">Become a CookieCrave Seller</h2>
                                        <p className="text-muted mb-4">
                                            List your cookies, managed orders, and grow your brand with our dedicated seller platform.
                                        </p>
                                        <div className="mb-4">
                                            <div className="d-flex align-items-center mb-2">
                                                <i className="bi bi-check2-circle text-success me-2 fs-5"></i>
                                                <span>Reach over 10,000+ customers</span>
                                            </div>
                                            <div className="d-flex align-items-center mb-2">
                                                <i className="bi bi-check2-circle text-success me-2 fs-5"></i>
                                                <span>Integrated SMS notifications</span>
                                            </div>
                                            <div className="d-flex align-items-center">
                                                <i className="bi bi-check2-circle text-success me-2 fs-5"></i>
                                                <span>Secure business dashboard</span>
                                            </div>
                                        </div>
                                        <Button 
                                            variant="danger" 
                                            className="w-100 fw-bold py-3 shadow-sm hover-up" 
                                            onClick={() => setShowSellerModal(true)}
                                            style={{transition: 'all 0.3s ease'}}
                                        >
                                            Register Now & Set Up Profile
                                        </Button>
                                    </div>
                                </Col>
                            </Row>
                        </Card>
                    </div>
                ) : (
                <div className="selling-section">
                    <Row>
                        <Col lg={4}>
                            <Card className="p-4 shadow-sm mb-4 border-0 bg-light">
                                <h4 className="fw-bold text-danger mb-1">₹{totalEarnings}</h4>
                                <div className="text-muted small uppercase fw-bold mb-0">Total Earnings</div>
                            </Card>
                            
                            <Card className="p-4 shadow-sm mb-4">
                                <h4 className="mb-4 fw-bold text-danger">
                                    <i className="bi bi-plus-circle me-2"></i> List a Cookie
                                </h4>
                                <Form onSubmit={handleCreateProduct}>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Cookie Name</Form.Label>
                                        <Form.Control type="text" value={productName} onChange={e => setProductName(e.target.value)} required placeholder="e.g. Choco Chip" />
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Description</Form.Label>
                                        <Form.Control as="textarea" rows={2} value={productDesc} onChange={e => setProductDesc(e.target.value)} required />
                                    </Form.Group>
                                    <Row>
                                        <Col>
                                            <Form.Group className="mb-3">
                                                <Form.Label>Price (₹)</Form.Label>
                                                <Form.Control type="number" step="0.01" value={productPrice} onChange={e => setProductPrice(e.target.value)} required />
                                            </Form.Group>
                                        </Col>
                                        <Col>
                                            <Form.Group className="mb-3">
                                                <Form.Label>Stock</Form.Label>
                                                <Form.Control type="number" value={productStock} onChange={e => setProductStock(e.target.value)} required />
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Category</Form.Label>
                                        <Form.Select value={productCat} onChange={e => setProductCat(e.target.value)} required>
                                            <option value="">Select Category</option>
                                            {categories.map(c => (
                                                <option key={c.id} value={c.id}>{c.name}</option>
                                            ))}
                                        </Form.Select>
                                    </Form.Group>
                                    <Form.Group className="mb-4">
                                        <Form.Label>Cookie Photo</Form.Label>
                                        <Form.Control type="file" accept="image/*" onChange={e => setProductImage(e.target.files[0])} />
                                    </Form.Group>
                                    <Button variant="danger" type="submit" className="w-100 fw-bold py-2">Publish Listing</Button>
                                </Form>
                            </Card>
                        </Col>
                        <Col lg={8}>
                            <Card className="p-4 shadow-sm mb-4">
                                <h4 className="mb-4 fw-bold text-danger">
                                    <i className="bi bi-journal-text me-2"></i> My Active Listings
                                </h4>
                                <Table responsive hover>
                                    <thead className="table-light">
                                        <tr>
                                            <th>Image</th>
                                            <th>Name</th>
                                            <th>Price</th>
                                            <th>Stock</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {myProducts.map(p => (
                                            <tr key={p.id} className="align-middle">
                                                <td>
                                                    <img src={p.image ? getProductImageUrl(p.image, getPlaceholderImageUrl('Cookie', 40, 40)) : 'https://placehold.co/40x40?text=🍪'} alt={p.name} style={{ width: '40px', height: '40px', borderRadius: '4px', objectFit: 'cover' }} crossOrigin="anonymous" />
                                                </td>
                                                <td>{p.name}</td>
                                                <td className="fw-bold">₹{p.price}</td>
                                                <td>
                                                    <Badge bg={p.stock > 0 ? "secondary" : "danger"}>{p.stock}</Badge>
                                                </td>
                                                <td>
                                                    <Button variant="outline-danger" size="sm" onClick={() => handleDeleteProduct(p.id)}>
                                                        <i className="bi bi-trash"></i>
                                                    </Button>
                                                </td>
                                            </tr>
                                        ))}
                                        {myProducts.length === 0 && (
                                            <tr>
                                                <td colSpan="4" className="text-center text-muted py-4">You haven't listed any cookies yet.</td>
                                            </tr>
                                        )}
                                    </tbody>
                                </Table>
                            </Card>

                            <Card className="p-4 shadow-sm">
                                <h4 className="mb-4 fw-bold text-danger">
                                    <i className="bi bi-graph-up-arrow me-2"></i> Recent Sales
                                </h4>
                                <Table responsive hover>
                                    <thead className="table-light">
                                        <tr>
                                            <th>Buyer</th>
                                            <th>Cookie</th>
                                            <th>Qty</th>
                                            <th>Total</th>
                                            <th>Date</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {transactions.filter(t => t.product_detail?.seller_username === currentUser).map(t => (
                                            <tr key={t.id}>
                                                <td>{t.user_username}</td>
                                                <td>{t.product_detail?.name}</td>
                                                <td>{t.quantity}</td>
                                                <td className="fw-bold text-danger">₹{t.total_price}</td>
                                                <td>{new Date(t.created_at).toLocaleDateString()}</td>
                                            </tr>
                                        ))}
                                        {transactions.filter(t => t.product_detail?.seller_username === currentUser).length === 0 && (
                                            <tr>
                                                <td colSpan="5" className="text-center text-muted py-4">No sales yet. Good luck!</td>
                                            </tr>
                                        )}
                                    </tbody>
                                </Table>
                            </Card>
                        </Col>
                    </Row>
                </div>
                )}
                </>
            )}
            
            <SellerRegisterModal 
                show={showSellerModal} 
                onHide={() => setShowSellerModal(false)} 
                onSecondarySuccess={handleRegistrationSuccess}
            />
        </div>
        </>
    );
};

export default Dashboard;
