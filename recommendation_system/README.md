# Cookie Recommendation System Documentation

## Overview
A comprehensive Netflix-style recommendation system for your cookie e-commerce platform. The system uses multiple algorithms to provide personalized product recommendations based on user behavior, preferences, and collaborative filtering.

## Features

### 🎯 Multiple Recommendation Algorithms
- **Personalized** - Based on user's viewing history and preferences
- **Collaborative Filtering** - Based on similar users' behavior
- **Content-Based** - Based on user's favorite categories and preferences
- **Popularity-Based** - Based on overall product popularity
- **Seasonal** - Based on current season/time of year
- **Trending** - Based on recent activity patterns
- **Hybrid** - Combination of multiple algorithms (default)

### 📊 Advanced Features
- **Feedback System** - Like/dislike/rating for recommendations
- **Preference Learning** - Track user's favorite categories, flavors, dietary needs
- **Performance Optimization** - Caching and efficient database queries
- **Analytics Integration** - Connect with existing user behavior data
- **Real-time Tracking** - Monitor clicks, purchases, and engagement

### 🔧 Database Models

#### UserPreference
Store user preferences and behavior patterns:
- Category preferences with weights
- Flavor preferences (favorite/disliked)
- Dietary restrictions and preferred ingredients
- Behavior patterns (price sensitivity, novelty seeking, brand loyalty)
- Time-based preferences (order times, seasonal preferences)

#### UserRecommendation
Store personalized recommendations with confidence scores:
- Product recommendations with algorithm source
- Confidence scores and reasoning
- Click/purchase tracking
- Expiration management

#### RecommendationFeedback
Track user feedback on recommendations:
- Multiple feedback types (like, dislike, not interested, etc.)
- Rating system (1-5 stars)
- Comments and suggestions

#### TrendingItem
Track trending products and categories:
- View/click/purchase/share counts
- Trending and velocity scores
- Multiple time periods (hourly, daily, weekly, monthly)

#### RecommendationHistory
Track user's recommendation history:
- Action tracking (viewed, clicked, purchased, feedback)
- Algorithm performance
- Context data (device, session, etc.)

#### RecommendationCache
Cache for pre-computed recommendations:
- Algorithm-specific caching
- Hit count tracking
- Automatic expiration

#### UserBehavior
Track detailed user behavior:
- Multiple behavior types (view, click, add_to_cart, purchase, etc.)
- Duration and quantity tracking
- Context information (session, device, referrer)

## API Endpoints

### Main Recommendations
```
GET /api/recommendations/recommendations/
```
**Query Parameters:**
- `algorithm` - Algorithm type (personalized, collaborative, content_based, popularity, seasonal, trending, hybrid)
- `limit` - Number of recommendations (default: 20, max: 100)
- `exclude_purchased` - Exclude already purchased items (default: true)
- `category_ids` - Filter by specific categories
- `price_range` - Price filter {"min": price, "max": price}

**Response:**
```json
{
  "recommendations": [...],
  "algorithm": "hybrid",
  "total_count": 20,
  "confidence_scores": {"product_id": score},
  "reasons": {"product_id": "reason"}
}
```

### Feedback System
```
POST /api/recommendations/feedback/
```
**Body:**
```json
{
  "recommendation_id": 123,
  "feedback_type": "like",
  "rating": 5,
  "comment": "Great recommendation!"
}
```

### User Preferences
```
GET /api/recommendations/preferences/
PUT /api/recommendations/preferences/
```

### Trending Items
```
GET /api/recommendations/trending/
```
**Query Parameters:**
- `period` - hourly, daily, weekly, monthly
- `category_id` - Filter by category
- `limit` - Number of items (default: 20)

### Statistics
```
GET /api/recommendations/stats/
```
**Query Parameters:**
- `period` - 1d, 7d, 30d

**Response:**
```json
{
  "total_recommendations": 100,
  "click_rate": 25.5,
  "purchase_rate": 12.3,
  "feedback_rate": 8.7,
  "algorithm_performance": {...},
  "category_performance": {...}
}
```

### Behavior Tracking
```
POST /api/recommendations/behavior/
```
**Body:**
```json
{
  "product_id": 123,
  "behavior_type": "view",
  "duration": 30,
  "session_id": "sess_123",
  "device_type": "mobile"
}
```

### Click Tracking
```
POST /api/recommendations/recommendations/{id}/click/
```

## Usage Examples

### Get Personalized Recommendations
```javascript
// Get hybrid recommendations for current user
const response = await fetch('/api/recommendations/recommendations/?algorithm=hybrid&limit=10');
const data = await response.json();
console.log(data.recommendations);
```

### Submit Feedback
```javascript
// Submit positive feedback
const feedback = await fetch('/api/recommendations/feedback/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    recommendation_id: 123,
    feedback_type: 'like',
    rating: 5
  })
});
```

### Update User Preferences
```javascript
// Update category preferences
const prefs = await fetch('/api/recommendations/preferences/', {
  method: 'PUT',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    category_preferences: {"1": 0.9, "2": 0.7},
    favorite_flavors: ["chocolate", "vanilla"],
    price_sensitivity: 0.8
  })
});
```

### Track User Behavior
```javascript
// Track product view
await fetch('/api/recommendations/behavior/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    product_id: 123,
    behavior_type: 'view',
    duration: 45,
    device_type: 'desktop'
  })
});
```

## Algorithm Details

### Personalized Algorithm
- Analyzes user's historical behavior (views, clicks, purchases)
- Calculates category preferences based on interaction weights
- Applies user preference adjustments (price sensitivity, novelty seeking)
- Excludes previously purchased items

### Collaborative Filtering
- Finds users with similar behavior patterns
- Recommends products liked by similar users
- Uses behavior weights (purchase=5, add_to_cart=3, click=2, view=1)
- Filters out items user already interacted with

### Content-Based
- Uses user's explicit category preferences
- Applies novelty preference for newer products
- Respects dietary restrictions and flavor preferences
- Balances exploration vs exploitation

### Popularity-Based
- Calculates popularity scores from all user behaviors
- Weights purchases higher than views/clicks
- Provides fallback recommendations when no personal data available
- Maintains diversity in recommendations

### Seasonal Algorithm
- Determines current season based on month
- Uses seasonal preferences if available
- Applies seasonal category boosts
- Falls back to random selection with seasonal context

### Trending Algorithm
- Analyzes recent activity patterns
- Calculates trending scores with velocity
- Updates in real-time based on user behavior
- Provides hot/new discoveries

### Hybrid Algorithm
- Combines multiple algorithms with weighted scores
- Algorithm weights: personalized (30%), collaborative (25%), content-based (20%), trending (15%), popularity (10%)
- Provides balanced recommendations
- Fallback handling for algorithm failures

## Performance Optimization

### Caching Strategy
- 1-hour cache for recommendation results
- Cache invalidation on preference changes
- Hit count tracking for cache optimization
- Automatic cleanup of expired cache entries

### Database Optimization
- Optimized indexes for frequent queries
- Efficient query patterns with select_related/prefetch_related
- Bulk operations for recommendation generation
- Connection pooling for high traffic

### Memory Management
- Generator-based recommendation processing
- Lazy loading of product data
- Efficient JSON field usage
- Periodic cleanup of old data

## Integration Points

### Existing Analytics
- Connects with user behavior tracking
- Enhances product recommendation analytics
- Provides recommendation performance metrics
- Supports A/B testing framework

### Product Catalog
- Real-time stock checking
- Category-based filtering
- Price range filtering
- New product highlighting

### User Management
- Automatic preference creation
- User profile integration
- Authentication-based access
- Privacy compliance

## Monitoring and Analytics

### Performance Metrics
- Recommendation generation time
- Cache hit rates
- Algorithm performance comparison
- User engagement rates

### Business Metrics
- Click-through rates
- Conversion rates
- Average order value impact
- Customer satisfaction

### Quality Metrics
- Feedback analysis
- Preference accuracy
- Recommendation diversity
- Cold start problem handling

## Configuration

### Environment Variables
```python
# Recommendation system settings
RECOMMENDATION_CACHE_TIMEOUT = 3600  # 1 hour
RECOMMENDATION_BATCH_SIZE = 100
RECOMMENDATION_MAX_RESULTS = 100
RECOMMENDATION_ENABLE_A_B_TESTING = True
```

### Algorithm Weights
```python
RECOMMENDATION_ALGORITHM_WEIGHTS = {
    'personalized': 0.3,
    'collaborative': 0.25,
    'content_based': 0.2,
    'trending': 0.15,
    'popularity': 0.1
}
```

## Troubleshooting

### Common Issues

1. **No Recommendations Returned**
   - Check if user has behavior history
   - Verify products have stock
   - Ensure categories exist

2. **Poor Recommendation Quality**
   - Check user preference data
   - Verify behavior tracking is working
   - Review algorithm weights

3. **Performance Issues**
   - Check cache hit rates
   - Monitor database query performance
   - Review indexing strategy

4. **Missing Feedback**
   - Verify feedback endpoints are called
   - Check user permissions
   - Review feedback processing logic

### Debug Mode
Enable debug logging:
```python
LOGGING = {
    'loggers': {
        'recommendation_system': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}
```

## Future Enhancements

### Planned Features
- Machine learning model integration
- Real-time recommendation updates
- Advanced A/B testing framework
- Cross-platform recommendation sync
- Voice-based preference input
- Image-based preference learning

### Scalability Improvements
- Distributed recommendation processing
- Redis clustering for cache
- Microservices architecture
- CDN integration for faster delivery

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check the Django admin interface
4. Monitor the system logs
5. Contact the development team

---

**Version**: 1.0.0  
**Last Updated**: 2025-03-10  
**Compatibility**: Django 4.0+, Python 3.8+
