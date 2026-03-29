import React, { useState, useRef, useEffect } from 'react';
import { Form, ListGroup } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import analytics from '../services/analyticsService';
import { getProductImageUrl } from '../utils/imageUtils';

const RECENT_SEARCHES_KEY = 'cookiecrave_recent_searches';
const MAX_RECENT = 10;

const getRecentSearches = () => {
  try {
    const stored = localStorage.getItem(RECENT_SEARCHES_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
};

const saveRecentSearch = (term) => {
  if (!term || !term.trim()) return;
  const trimmed = term.trim();
  let recent = getRecentSearches().filter(s => s.toLowerCase() !== trimmed.toLowerCase());
  recent = [trimmed, ...recent].slice(0, MAX_RECENT);
  localStorage.setItem(RECENT_SEARCHES_KEY, JSON.stringify(recent));
};

const clearRecentSearches = () => {
  localStorage.removeItem(RECENT_SEARCHES_KEY);
};

const getProductImage = (p) => {
  return getProductImageUrl(p?.image, 'https://placehold.co/60x60?text=🍪');
};

const NavSearchBar = () => {
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState([]);
  const [recentSearches, setRecentSearches] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const wrapperRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        const res = await api.get('products/');
        setProducts(res.data || []);
      } catch {
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleFocus = () => {
    setRecentSearches(getRecentSearches());
    setShowDropdown(true);
  };

  const handleChange = (e) => {
    const newQuery = e.target.value;
    setQuery(newQuery);
    setShowDropdown(true);
    
    // If search is cancelled (empty query), redirect to home page
    if (!newQuery.trim()) {
      navigate('/home');
    }
  };

  const filterProducts = () => {
    if (!query.trim()) return [];
    const q = query.toLowerCase();
    return products.filter(p => {
      const name = (p.name || '').toLowerCase();
      const desc = (p.description || '').toLowerCase();
      const cat = (p.category_name || '').toLowerCase();
      return name.includes(q) || desc.includes(q) || cat.includes(q);
    }).slice(0, 8);
  };

  const handleSelectProduct = (product) => {
    // Track product selection from search
    analytics.track('search_product_select', {
      product_id: product.id,
      product_name: product.name,
      product_price: product.price,
      search_query: query,
      result_position: filteredProducts.findIndex(p => p.id === product.id) + 1
    });
    
    saveRecentSearch(product.name);
    setQuery('');
    setShowDropdown(false);
    navigate(`/home?product=${product.id}`);
  };

  const handleSelectRecent = (term) => {
    // Track recent search selection
    analytics.track('search_recent_select', {
      search_query: term,
      is_recent_search: true
    });
    
    setQuery(term);
    saveRecentSearch(term);
    setShowDropdown(false);
    navigate(`/home?q=${encodeURIComponent(term)}`);
  };

  const handleClearRecent = (e) => {
    e.stopPropagation();
    clearRecentSearches();
    setRecentSearches([]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      // Track search submission
      analytics.track('search_submit', {
        search_query: query.trim(),
        result_count: filteredProducts.length,
        search_type: 'manual'
      });
      
      saveRecentSearch(query.trim());
      setShowDropdown(false);
      navigate(`/home?q=${encodeURIComponent(query.trim())}`);
    }
  };

  const filteredProducts = filterProducts();
  const hasResults = filteredProducts.length > 0;
  const showRecent = showDropdown && !query.trim();
  const showProductResults = showDropdown && query.trim();

  return (
    <div ref={wrapperRef} className="position-relative me-3" style={{ minWidth: 220, maxWidth: 320 }}>
      <Form onSubmit={handleSubmit}>
        <Form.Control
          type="search"
          placeholder="Search cookies..."
          value={query}
          onChange={handleChange}
          onFocus={handleFocus}
          className="rounded-pill border-0 ps-3 pe-4 nav-search-input"
          style={{ paddingTop: 8, paddingBottom: 8 }}
          autoComplete="off"
        />
        <span className="position-absolute end-0 top-50 translate-middle-y me-3 text-muted" style={{ pointerEvents: 'none' }}>
          <i className="bi bi-search"></i>
        </span>
      </Form>

      {showRecent && (
        <ListGroup className="position-absolute top-100 start-0 end-0 mt-1 shadow-lg border-0 rounded-3 overflow-hidden" style={{ zIndex: 1050 }}>
          {recentSearches.length > 0 ? (
            <>
              <ListGroup.Item className="d-flex justify-content-between align-items-center py-2 bg-light">
                <small className="text-muted fw-bold">Recent</small>
                <button type="button" className="btn btn-link btn-sm p-0 text-muted" onClick={handleClearRecent}>Clear</button>
              </ListGroup.Item>
              {recentSearches.map((term, i) => (
                <ListGroup.Item key={i} action onClick={() => handleSelectRecent(term)} className="d-flex align-items-center py-2">
                  <i className="bi bi-clock-history me-2 text-muted"></i>
                  {term}
                </ListGroup.Item>
              ))}
            </>
          ) : (
            <ListGroup.Item className="text-muted small py-3 text-center">No recent searches</ListGroup.Item>
          )}
        </ListGroup>
      )}

      {showProductResults && (
        <ListGroup className="position-absolute top-100 start-0 end-0 mt-1 shadow-lg border-0 rounded-3 overflow-hidden" style={{ zIndex: 1050, maxHeight: 360 }}>
          {loading ? (
            <ListGroup.Item className="py-4 text-center text-muted">Loading...</ListGroup.Item>
          ) : hasResults ? (
            filteredProducts.map((p) => (
              <ListGroup.Item
                key={p.id}
                action
                onClick={() => handleSelectProduct(p)}
                className="d-flex align-items-center py-2"
              >
                <img
                  src={getProductImage(p)}
                  alt={p.name}
                  style={{ width: 44, height: 44, objectFit: 'cover', borderRadius: 8 }}
                  crossOrigin="anonymous"
                  onError={(e) => { e.target.onerror = null; e.target.src = 'https://placehold.co/44x44?text=🍪'; }}
                />
                <div className="ms-3 flex-grow-1 min-w-0">
                  <div className="fw-semibold" style={{ wordWrap: 'break-word', whiteSpace: 'normal' }}>{p.name}</div>
                  <small className="text-muted">₹{p.price}</small>
                </div>
              </ListGroup.Item>
            ))
          ) : (
            <ListGroup.Item className="text-muted small py-3 text-center">No results for "{query}"</ListGroup.Item>
          )}
        </ListGroup>
      )}
    </div>
  );
};

export default NavSearchBar;
