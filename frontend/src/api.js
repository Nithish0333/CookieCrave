import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/',
});

// Attach access token to every request (if available)
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access') || sessionStorage.getItem('access');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Auto-refresh token on 401 responses
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If 401 and we haven't already tried to refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const refresh = localStorage.getItem('refresh') || sessionStorage.getItem('refresh');
            if (refresh) {
                try {
                    const res = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/'}users/token/refresh/`, {
                        refresh,
                    });
                    const newAccess = res.data.access;

                    // Store the new access token wherever the old one was
                    if (localStorage.getItem('refresh')) {
                        localStorage.setItem('access', newAccess);
                    } else {
                        sessionStorage.setItem('access', newAccess);
                    }

                    // Retry the original request with new token
                    originalRequest.headers.Authorization = `Bearer ${newAccess}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    // Refresh failed — clear tokens and redirect to login
                    localStorage.removeItem('access');
                    localStorage.removeItem('refresh');
                    sessionStorage.removeItem('access');
                    sessionStorage.removeItem('refresh');
                    window.location.href = '/login';
                    return Promise.reject(refreshError);
                }
            } else {
                // No refresh token — redirect to login
                window.location.href = '/login';
            }
        }

        return Promise.reject(error);
    }
);

// Recommendation API functions
export const recommendationAPI = {
    getRecommendations: (algorithm = 'hybrid', limit = 12, categoryIds = null, priceRange = null) => {
        const params = new URLSearchParams({
            algorithm,
            limit,
            exclude_purchased: true,
        });
        
        if (categoryIds && categoryIds.length > 0) {
            params.append('category_ids', categoryIds.join(','));
        }
        
        if (priceRange) {
            if (priceRange.min !== undefined) {
                params.append('price_range[min]', priceRange.min);
            }
            if (priceRange.max !== undefined) {
                params.append('price_range[max]', priceRange.max);
            }
        }
        
        return api.get(`recommendations/recommendations/?${params}`);
    },
    
    getTrending: (limit = 10) => {
        return api.get('recommendations/trending/', { params: { limit } });
    },
    
    getUserPreferences: () => {
        return api.get('recommendations/preferences/');
    },
    
    updateUserPreferences: (preferences) => {
        return api.post('recommendations/preferences/', preferences);
    },
    
    submitFeedback: (recommendationId, feedbackType, rating = null, comment = '') => {
        return api.post('recommendations/feedback/', {
            recommendation_id: recommendationId,
            feedback_type: feedbackType,
            rating,
            comment,
        });
    },
    
    trackRecommendationClick: (recommendationId) => {
        return api.post(`recommendations/recommendations/${recommendationId}/click/`);
    },
    
    getStats: () => {
        return api.get('recommendations/stats/');
    },
};

export default api;
