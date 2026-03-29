import React, { useState, useRef, useEffect } from 'react';
import { Form, ListGroup } from 'react-bootstrap';

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

const SearchBar = ({ value, onChange, onSearch, placeholder = "Search cookies..." }) => {
  const [showRecent, setShowRecent] = useState(false);
  const [recentSearches, setRecentSearches] = useState(getRecentSearches);
  const wrapperRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowRecent(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleFocus = () => {
    setRecentSearches(getRecentSearches());
    setShowRecent(true);
  };

  const handleSelectRecent = (term) => {
    onChange(term);
    onSearch?.(term);
    setShowRecent(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (value?.trim()) {
      saveRecentSearch(value.trim());
      setRecentSearches(getRecentSearches());
      onSearch?.(value.trim());
    }
    setShowRecent(false);
  };

  const handleClearRecent = (e) => {
    e.stopPropagation();
    clearRecentSearches();
    setRecentSearches([]);
  };

  return (
    <div ref={wrapperRef} className="position-relative" style={{ maxWidth: 400 }}>
      <Form onSubmit={handleSubmit}>
        <Form.Control
          type="search"
          placeholder={placeholder}
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          onFocus={handleFocus}
          className="rounded-pill ps-4 pe-5"
          style={{ paddingTop: 10, paddingBottom: 10 }}
          autoComplete="off"
        />
        <span 
          className="position-absolute end-0 top-50 translate-middle-y me-3 text-muted"
          style={{ pointerEvents: 'none' }}
        >
          <i className="bi bi-search"></i>
        </span>
      </Form>

      {showRecent && (
        <ListGroup 
          className="position-absolute top-100 start-0 end-0 mt-1 shadow-sm border rounded-3 overflow-hidden"
          style={{ zIndex: 1050 }}
        >
          {recentSearches.length > 0 ? (
            <>
              <ListGroup.Item className="d-flex justify-content-between align-items-center py-2 bg-light">
                <small className="text-muted fw-bold">Recent searches</small>
                <button
                  type="button"
                  className="btn btn-link btn-sm p-0 text-muted"
                  onClick={handleClearRecent}
                >
                  Clear
                </button>
              </ListGroup.Item>
              {recentSearches.map((term, i) => (
                <ListGroup.Item
                  key={i}
                  action
                  onClick={() => handleSelectRecent(term)}
                  className="d-flex align-items-center py-2"
                >
                  <i className="bi bi-clock-history me-2 text-muted"></i>
                  {term}
                </ListGroup.Item>
              ))}
            </>
          ) : (
            <ListGroup.Item className="text-muted small py-3 text-center">
              No recent searches
            </ListGroup.Item>
          )}
        </ListGroup>
      )}
    </div>
  );
};

export default SearchBar;
