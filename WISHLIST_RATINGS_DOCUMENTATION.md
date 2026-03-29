# Wishlist and Ratings Feature Documentation

## Overview

This document describes the new Wishlist and Ratings features added to the CookieCrave application. These features allow users to save products they're interested in and provide ratings and reviews for products they've purchased.

## Backend Implementation

### Database Models

#### 1. Wishlist Model
Located in: `backend/products/models.py`

```python
class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Features:**
- One-to-one relationship with User (each user has one wishlist)
- Many-to-many relationship with Product (one wishlist can contain many products)
- Automatic timestamps for creation and updates

#### 2. Rating Model
Located in: `backend/products/models.py`

```python
class Rating(models.Model):
    RATING_CHOICES = [(1, '1 Star'), (2, '2 Stars'), ..., (5, '5 Stars')]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'product')  # Each user can only rate a product once
```

**Features:**
- Foreign key relationship with User and Product
- Star ratings (1-5)
- Optional text review
- Unique constraint: each user can only rate a product once
- Automatic timestamps for creation and updates

### API Endpoints

#### Wishlist Endpoints

**GET /api/products/wishlist/**
- Retrieves the current user's wishlist
- Returns wishlist with product details
- Authentication: Required

**POST /api/products/wishlist/add_product/**
- Adds a product to the user's wishlist
- Request body: `{ "product_id": <int> }`
- Returns updated wishlist
- Authentication: Required

**POST /api/products/wishlist/remove_product/**
- Removes a product from the user's wishlist
- Request body: `{ "product_id": <int> }`
- Returns updated wishlist
- Authentication: Required

#### Rating Endpoints

**GET /api/products/ratings/**
- Lists all ratings (optionally filtered by product)
- Query parameters: `product_id` (optional)
- Returns list of ratings with user and product details
- Authentication: Not required for reading

**POST /api/products/ratings/**
- Creates a new rating for a product
- Request body:
  ```json
  {
    "product": <int>,
    "rating": <1-5>,
    "review": "<optional text>"
  }
  ```
- Returns the created rating
- Authentication: Required

**PATCH /api/products/ratings/<id>/**
- Updates an existing rating
- Request body: (same as POST, all fields optional except product)
- Returns the updated rating
- Authentication: Required

**GET /api/products/ratings/<id>/**
- Retrieves a specific rating
- Authentication: Not required for reading

### Database Migration

A migration file has been created: `backend/products/migrations/0006_add_wishlist_rating.py`

To apply the migration:
```bash
python manage.py migrate products
```

## Frontend Implementation

### Components

#### 1. WishlistPage Component
Located in: `frontend/src/pages/WishlistPage.jsx`

**Features:**
- Display all products in the user's wishlist
- Remove products from wishlist
- Product information display (name, description, price, stock)
- Responsive grid layout
- Toast notifications for user actions
- Analytics tracking

**Usage:**
```jsx
import WishlistPage from './pages/WishlistPage';
```

#### 2. WishlistButton Component
Located in: `frontend/src/components/WishlistButton.jsx`

**Features:**
- Toggle button to add/remove products from wishlist
- Visual feedback (filled/outline heart)
- Toast notifications
- Analytics tracking
- Responsive sizing with `className` prop

**Usage:**
```jsx
import WishlistButton from './components/WishlistButton';

<WishlistButton 
  productId={product.id} 
  productName={product.name}
  className="mb-2"
/>
```

#### 3. RatingComponent Component
Located in: `frontend/src/components/RatingComponent.jsx`

**Features:**
- Display averaged product ratings
- Show rating distribution histogram
- Allow users to submit/update ratings
- Display all reviews for a product
- Interactive star rating selector
- Analytics tracking

**Usage:**
```jsx
import RatingComponent from './components/RatingComponent';

<RatingComponent 
  productId={product.id}
  productName={product.name}
/>
```

### App Routes

The following routes have been added to `frontend/src/App.jsx`:

- `/wishlist` - Wishlist page (protected route)
- Navigation link for wishlist in the navbar

### Integration Examples

#### Adding Wishlist Button to Product Cards
```jsx
import WishlistButton from '../components/WishlistButton';

const ProductCard = ({ product }) => {
  return (
    <Card>
      <Card.Body>
        <Card.Title>{product.name}</Card.Title>
        <WishlistButton 
          productId={product.id}
          productName={product.name}
        />
      </Card.Body>
    </Card>
  );
};
```

#### Adding Ratings to Product Details Page
```jsx
import RatingComponent from '../components/RatingComponent';

const ProductDetailsPage = ({ product }) => {
  return (
    <Container>
      <h1>{product.name}</h1>
      {/* Product details... */}
      <RatingComponent 
        productId={product.id}
        productName={product.name}
      />
    </Container>
  );
};
```

## Admin Interface

Both models are registered in the Django admin:

**Wishlist Admin:**
- View all wishlists
- Filter by creation date
- Search by username
- View product count for each wishlist

**Rating Admin:**
- View all ratings
- Filter by star rating and creation date
- Search by username, product name, or review text
- Change created/updated timestamps

Access at: `http://localhost:8000/admin/`

## Data Flow

### Wishlist Flow
1. User clicks "Add to Wishlist" button on a product
2. WishlistButton component sends POST request to `/api/products/wishlist/add_product/`
3. Backend retrieves or creates user's wishlist
4. Product is added to wishlist's many-to-many relationship
5. Frontend updates UI and shows confirmation toast
6. Analytics event is tracked

### Rating Flow
1. User fills in rating form on product page
2. RatingComponent sends POST/PATCH request to `/api/products/ratings/`
3. Backend validates rating uniqueness (user + product)
4. Rating is created or updated in database
5. Frontend refetches all ratings and updates display
6. Analytics event is tracked

## Analytics Events

The following analytics events are tracked:

**Wishlist Events:**
- `product_added_to_wishlist` - When a product is added
- `product_removed_from_wishlist` - When a product is removed

**Rating Events:**
- `product_rated` - When a rating is submitted/updated
  - Includes: product_id, product_name, rating value, has_review

## Security Considerations

1. **Authentication:** Wishlist and rating creation endpoints require authentication
2. **Authorization:** Users can only manage their own wishlist and ratings
3. **Unique Constraint:** Database-enforced constraint prevents duplicate user-product ratings
4. **Read Access:** Anyone can view ratings (not authenticated)
5. **CSRF Protection:** Django's CSRF middleware protects POST requests

## Performance Considerations

1. **Database Queries:**
   - Wishlist uses select_related to fetch products efficiently
   - Rating queries are filtered by product_id to limit result sets

2. **Caching Recommendations:**
   - Consider caching product rating averages for frequently rated products
   - Cache wishlist queries for authenticated users

3. **Scalability:**
   - Consider adding pagination to ratings list if products have many reviews
   - Implement rating caching at the ORM or Redis level for high-traffic products

## Future Enhancements

1. **Wishlist Features:**
   - Share wishlist with other users
   - Wishlist categories/folders
   - Email notifications when wishlist items go on sale
   - Price tracking for wishlist items

2. **Rating Features:**
   - Helpful/unhelpful votes on reviews
   - Rating filtering and sorting
   - Seller response to reviews
   - Verified purchase badges
   - Image/video attachments in reviews
   - Rating badges (Top Reviewer, etc.)

3. **Social Features:**
   - Follow other users' wishlists
   - Compare wishlists with friends
   - Share ratings on social media

## Troubleshooting

### Migration Issues
```bash
# If migration fails, check migration dependencies
python manage.py showmigrations products

# Roll back if needed
python manage.py migrate products 0005_add_category_image_url
```

### API Errors
- 401 Unauthorized: User must be logged in for wishlist and rating creation
- 404 Not Found: Product ID doesn't exist
- 400 Bad Request: Invalid rating value (must be 1-5)

### Frontend Issues
- Ensure `api` module is properly imported
- Verify authentication token is stored in localStorage as 'access'
- Check browser console for CORS errors if connecting to different domain
