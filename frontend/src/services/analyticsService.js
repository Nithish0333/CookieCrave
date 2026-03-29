import api from '../api';

class AnalyticsService {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.queue = [];
        this.isOnline = navigator.onLine;
        this.startTime = Date.now();
        this.lastPageView = null;
        this.scrollDepth = 0;
        this.maxScrollDepth = 0;
        
        // Initialize tracking
        this.init();
    }

    generateSessionId() {
        // Check if session ID exists in sessionStorage
        let sessionId = sessionStorage.getItem('analytics_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('analytics_session_id', sessionId);
        }
        return sessionId;
    }

    init() {
        // Track session start
        this.trackEvent('session_start', {
            user_agent: navigator.userAgent,
            screen_resolution: `${screen.width}x${screen.height}`,
            viewport_size: `${window.innerWidth}x${window.innerHeight}`,
            language: navigator.language,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            referrer: document.referrer
        });

        // Track page view on initial load
        this.trackPageView();

        // Set up event listeners
        this.setupEventListeners();

        // Set up periodic queue processing
        setInterval(() => this.processQueue(), 5000);

        // Track session end on page unload
        window.addEventListener('beforeunload', () => {
            this.trackSessionEnd();
        });

        // Track visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.trackPageLeave();
            } else {
                this.trackPageView();
            }
        });
    }

    setupEventListeners() {
        // Track clicks
        document.addEventListener('click', (event) => {
            this.trackClick(event);
        }, true);

        // Track scroll behavior
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.trackScroll();
            }, 100);
        });

        // Track search interactions
        document.addEventListener('submit', (event) => {
            if (event.target.tagName === 'FORM') {
                const searchInput = event.target.querySelector('input[type="search"], input[name="q"], input[name="search"]');
                if (searchInput && searchInput.value) {
                    this.trackSearch(searchInput.value);
                }
            }
        });

        // Track add to cart actions
        document.addEventListener('click', (event) => {
            const target = event.target;
            if (target.matches('[data-track="add-to-cart"], .add-to-cart, button:contains("Add to Cart")') ||
                target.closest('[data-track="add-to-cart"], .add-to-cart')) {
                this.trackAddToCart(event);
            }
        });

        // Track purchase actions
        document.addEventListener('click', (event) => {
            const target = event.target;
            if (target.matches('[data-track="purchase"], .purchase, button:contains("Buy"), button:contains("Purchase")') ||
                target.closest('[data-track="purchase"], .purchase')) {
                this.trackPurchase(event);
            }
        });
    }

    trackEvent(actionType, metadata = {}) {
        const eventData = {
            session_id: this.sessionId,
            action_type: actionType,
            page_url: window.location.href,
            page_title: document.title,
            timestamp: new Date().toISOString(),
            metadata: {
                ...metadata,
                viewport_width: window.innerWidth,
                viewport_height: window.innerHeight
            }
        };

        this.queue.push(eventData);
        this.processQueue();
    }

    trackPageView() {
        const now = Date.now();
        let timeOnPage = 0;

        if (this.lastPageView) {
            timeOnPage = Math.floor((now - this.lastPageView) / 1000);
        }

        this.lastPageView = now;
        
        // Determine specific page type based on URL
        const actionType = this.getPageActionType();
        
        this.trackEvent(actionType, {
            time_on_page: timeOnPage,
            scroll_depth: this.maxScrollDepth
        });

        // Reset scroll tracking for new page
        this.scrollDepth = 0;
        this.maxScrollDepth = 0;
    }

    getPageActionType() {
        const path = window.location.pathname.toLowerCase();
        
        if (path === '/' || path === '/home' || path.includes('/home')) {
            return 'home_page_view';
        } else if (path.includes('/about')) {
            return 'about_page_view';
        } else if (path.includes('/contact')) {
            return 'contact_page_view';
        } else if (path.includes('/dashboard') || path.includes('/selling')) {
            return 'selling_page_view';
        } else if (path.includes('/cart') || path.includes('/purchase')) {
            return 'purchase_page_view';
        } else {
            return 'page_view'; // Default page view
        }
    }

    trackHomePageView() {
        this.trackEvent('home_page_view', {
            page_category: 'home'
        });
    }

    trackAboutPageView() {
        this.trackEvent('about_page_view', {
            page_category: 'about'
        });
    }

    trackContactPageView() {
        this.trackEvent('contact_page_view', {
            page_category: 'contact'
        });
    }

    trackSellingPageView() {
        this.trackEvent('selling_page_view', {
            page_category: 'selling'
        });
    }

    trackPurchasePageView() {
        this.trackEvent('purchase_page_view', {
            page_category: 'purchase'
        });
    }

    trackPageLeave() {
        if (this.lastPageView) {
            const timeOnPage = Math.floor((Date.now() - this.lastPageView) / 1000);
            this.trackEvent('page_leave', {
                time_on_page: timeOnPage,
                scroll_depth: this.maxScrollDepth
            });
        }
    }

    trackClick(event) {
        const target = event.target;
        const rect = target.getBoundingClientRect();
        
        // Track click position for heatmap
        this.trackHeatmapClick(event);

        const clickData = {
            button_text: target.textContent?.trim() || target.value || '',
            element_selector: this.getSelector(target),
            element_tag: target.tagName.toLowerCase(),
            element_id: target.id || '',
            element_class: target.className || '',
            click_x: event.clientX,
            click_y: event.clientY,
            viewport_x: rect.left,
            viewport_y: rect.top
        };

        // Check if it's a product view
        const productLink = target.closest('[data-product-id], .product-link, .product-card');
        if (productLink) {
            const productId = productLink.dataset.productId || 
                            productLink.querySelector('[data-product-id]')?.dataset.productId;
            if (productId) {
                this.trackProductView(productId, clickData);
                return;
            }
        }

        this.trackEvent('button_click', clickData);
    }

    trackHeatmapClick(event) {
        const heatmapData = {
            page_url: window.location.href,
            click_x: event.clientX,
            click_y: event.clientY,
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight,
            session_id: this.sessionId
        };

        // Send heatmap data separately
        this.sendHeatmapData(heatmapData);
    }

    trackScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercentage = scrollHeight > 0 ? Math.round((scrollTop / scrollHeight) * 100) : 0;

        this.scrollDepth = scrollPercentage;
        this.maxScrollDepth = Math.max(this.maxScrollDepth, scrollPercentage);

        // Track significant scroll milestones
        if (scrollPercentage === 25 || scrollPercentage === 50 || scrollPercentage === 75 || scrollPercentage === 90) {
            this.trackEvent('scroll', {
                scroll_depth: scrollPercentage,
                scroll_milestone: true
            });
        }
    }

    trackSearch(query) {
        this.trackEvent('search', {
            search_query: query.trim()
        });
    }

    trackProductView(productId, additionalData = {}) {
        this.trackEvent('product_view', {
            product_id: productId,
            ...additionalData
        });
    }

    trackAddToCart(event) {
        const target = event.target;
        const productCard = target.closest('[data-product-id], .product-card');
        const productId = productCard?.dataset.productId;
        
        this.trackEvent('add_to_cart', {
            product_id: productId,
            button_text: target.textContent?.trim() || '',
            element_selector: this.getSelector(target)
        });
    }

    trackPurchase(event) {
        const target = event.target;
        
        this.trackEvent('purchase', {
            button_text: target.textContent?.trim() || '',
            element_selector: this.getSelector(target),
            purchase_value: this.extractPurchaseValue(target)
        });
    }

    trackSessionEnd() {
        const sessionDuration = Math.floor((Date.now() - this.startTime) / 1000);
        
        this.trackEvent('session_end', {
            session_duration: sessionDuration,
            total_page_views: this.getPageViewCount(),
            max_scroll_depth: this.maxScrollDepth
        });
    }

    getSelector(element) {
        if (element.id) {
            return `#${element.id}`;
        }
        
        let selector = element.tagName.toLowerCase();
        
        if (element.className) {
            const classes = element.className.split(' ').filter(c => c.trim());
            if (classes.length > 0) {
                selector += '.' + classes.join('.');
            }
        }
        
        return selector;
    }

    extractPurchaseValue(element) {
        // Try to extract purchase value from nearby elements
        const parent = element.closest('.product-card, .purchase-container, .cart-item');
        if (parent) {
            const priceElement = parent.querySelector('.price, [data-price], .amount');
            if (priceElement) {
                const priceText = priceElement.textContent.trim();
                const price = parseFloat(priceText.replace(/[^0-9.]/g, ''));
                return isNaN(price) ? null : price;
            }
        }
        return null;
    }

    getPageViewCount() {
        return this.queue.filter(event => event.action_type === 'page_view').length;
    }

    async processQueue() {
        if (this.queue.length === 0 || !this.isOnline) return;

        const eventsToSend = this.queue.splice(0, 10); // Send up to 10 events at once

        try {
            await api.post('/analytics/behaviors/bulk_track/', {
                behaviors: eventsToSend
            });
        } catch (error) {
            console.error('Analytics tracking failed:', error);
            // Re-queue failed events
            this.queue.unshift(...eventsToSend);
        }
    }

    async sendHeatmapData(heatmapData) {
        try {
            await api.post('/analytics/heatmap/', heatmapData);
        } catch (error) {
            console.error('Heatmap tracking failed:', error);
        }
    }

    // Public API methods
    page(path, title) {
        // Track manual page navigation
        this.trackPageView();
    }

    identify(userId, traits = {}) {
        // Associate session with user
        this.trackEvent('user_identified', {
            user_id: userId,
            traits
        });
    }

    track(eventName, properties = {}) {
        this.trackEvent(eventName, properties);
    }

    // Utility methods
    getTimeOnPage() {
        return this.lastPageView ? Math.floor((Date.now() - this.lastPageView) / 1000) : 0;
    }

    getScrollDepth() {
        return this.maxScrollDepth;
    }

    getSessionInfo() {
        return {
            session_id: this.sessionId,
            start_time: this.startTime,
            time_on_page: this.getTimeOnPage(),
            scroll_depth: this.getScrollDepth()
        };
    }
}

// Create and export singleton instance
const analytics = new AnalyticsService();
export default analytics;
