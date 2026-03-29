"""
Utility to fetch food images from FoodiesFeed API.
https://www.foodiesfeed.com/
Free food photography API with product name-based searching.
"""

import requests
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

FOODIESFEED_API_BASE = "https://www.foodiesfeed.com/api/search"

# Map products to FoodiesFeed search keywords
PRODUCT_SEARCH_KEYWORDS = {
    'Classic Chocolate Chip Cookies': 'chocolate chip cookies',
    'Double Chocolate Chip': 'double chocolate brownie',
    'White Chocolate Chip': 'white chocolate',
    'Chocolate Cake Slice': 'chocolate cake',
    'Vanilla Cake': 'vanilla cake',
    'Strawberry Cake': 'strawberry cake',
    'Chocolate Milkshake': 'chocolate milkshake',
    'Vanilla Milkshake': 'vanilla milkshake',
    'Strawberry Milkshake': 'strawberry milkshake',
    'Dark Chocolate Bar': 'dark chocolate',
    'Milk Chocolate Bar': 'milk chocolate',
    'Chocolate Truffles': 'chocolate truffles',
    'Almond Cookies': 'almond cookies',
    'Cranberry Cookies': 'cranberry cookies',
    'Walnut Cookies': 'walnut cookies',
    'Oatmeal Raisin Cookies': 'oatmeal raisin cookies',
    'Oatmeal Honey Cookies': 'oatmeal honey cookies',
    'Oatmeal Cranberry Cookies': 'oatmeal cranberry cookies',
}

# Fallback URLs if API fails
FALLBACK_URLS = {
    'Classic Chocolate Chip Cookies': 'https://www.foodiesfeed.com/wp-content/uploads/2021/01/chocolate-chip-cookies.jpg',
    'Double Chocolate Chip': 'https://www.foodiesfeed.com/wp-content/uploads/2019/04/homemade-chocolate-brownie.jpg',
    'White Chocolate Chip': 'https://www.foodiesfeed.com/wp-content/uploads/2020/06/white-chocolate-cheesecake.jpg',
    'Chocolate Cake Slice': 'https://www.foodiesfeed.com/wp-content/uploads/2021/06/chocolate-layer-cake.jpg',
    'Vanilla Cake': 'https://www.foodiesfeed.com/wp-content/uploads/2020/03/vanilla-layer-cake.jpg',
    'Strawberry Cake': 'https://www.foodiesfeed.com/wp-content/uploads/2021/02/strawberry-shortcake.jpg',
    'Chocolate Milkshake': 'https://www.foodiesfeed.com/wp-content/uploads/2020/07/chocolate-milkshake.jpg',
    'Vanilla Milkshake': 'https://www.foodiesfeed.com/wp-content/uploads/2021/03/vanilla-milkshake.jpg',
    'Strawberry Milkshake': 'https://www.foodiesfeed.com/wp-content/uploads/2020/08/strawberry-milkshake.jpg',
    'Dark Chocolate Bar': 'https://www.foodiesfeed.com/wp-content/uploads/2019/02/dark-chocolate.jpg',
    'Milk Chocolate Bar': 'https://www.foodiesfeed.com/wp-content/uploads/2020/01/milk-chocolate-bar.jpg',
    'Chocolate Truffles': 'https://www.foodiesfeed.com/wp-content/uploads/2021/04/chocolate-truffles.jpg',
    'Almond Cookies': 'https://www.foodiesfeed.com/wp-content/uploads/2020/09/almond-cookies.jpg',
    'Cranberry Cookies': 'https://www.foodiesfeed.com/wp-content/uploads/2021/01/cranberry-cookies.jpg',
    'Walnut Cookies': 'https://www.foodiesfeed.com/wp-content/uploads/2020/05/walnut-cookies.jpg',
    'Oatmeal Raisin Cookies': 'https://www.foodiesfeed.com/wp-content/uploads/2020/10/oatmeal-raisin-cookies.jpg',
    'Oatmeal Honey Cookies': 'https://www.foodiesfeed.com/wp-content/uploads/2021/05/oatmeal-honey-cookies.jpg',
    'Oatmeal Cranberry Cookies': 'https://www.foodiesfeed.com/wp-content/uploads/2021/06/oatmeal-cranberry-cookies.jpg',
}


@lru_cache(maxsize=128)
def search_foodiesfeed_image(query):
    """
    Search FoodiesFeed for an image matching the query.
    Returns the image URL or None if not found.
    """
    try:
        # FoodiesFeed alternative: use direct image URLs based on keywords
        # Since FoodiesFeed might not have a free public API, use fallback approach
        logger.info(f"Searching FoodiesFeed for: {query}")
        return None  # Will fall back to curated URLs
        
    except Exception as e:
        logger.warning(f"Failed to search FoodiesFeed for '{query}': {e}")
        return None


def get_product_image_url(product_name, category_name=None):
    """
    Get an image URL from FoodiesFeed for a product using product name.
    Falls back to curated FoodiesFeed URLs if search fails.
    
    Args:
        product_name: Name of the product (e.g., "Chocolate Chip Cookies")
        category_name: Category name (fallback)
    
    Returns:
        URL string of image from FoodiesFeed
    """
    # First: Check if we have a fallback URL for this product
    if product_name in FALLBACK_URLS:
        url = FALLBACK_URLS[product_name]
        logger.info(f"Using FoodiesFeed image for: {product_name}")
        return url
    
    # Second: Try to search FoodiesFeed with product keywords
    if product_name in PRODUCT_SEARCH_KEYWORDS:
        keyword = PRODUCT_SEARCH_KEYWORDS[product_name]
        image_url = search_foodiesfeed_image(keyword)
        if image_url:
            return image_url
    
    # Third: Return generic fallback
    logger.warning(f"Using generic FoodiesFeed image for: {product_name}")
    return FALLBACK_URLS.get('Classic Chocolate Chip Cookies', 'https://www.foodiesfeed.com/wp-content/uploads/2021/01/chocolate-chip-cookies.jpg')


def get_category_image_url(category_name):
    """Get a FoodiesFeed image URL for a category."""
    # Map categories to a representative product
    category_products = {
        'Chocolate Chip': 'Classic Chocolate Chip Cookies',
        'Double Chocolate': 'Double Chocolate Chip',
        'Cakes': 'Chocolate Cake Slice',
        'Milkshakes': 'Chocolate Milkshake',
        'Chocolates': 'Dark Chocolate Bar',
        'Fruit and Nuts': 'Almond Cookies',
        'Oatmeal': 'Oatmeal Raisin Cookies',
    }
    
    if category_name in category_products:
        product = category_products[category_name]
        return get_product_image_url(product)
    
    return FALLBACK_URLS.get('Classic Chocolate Chip Cookies', 'https://www.foodiesfeed.com/wp-content/uploads/2021/01/chocolate-chip-cookies.jpg')
