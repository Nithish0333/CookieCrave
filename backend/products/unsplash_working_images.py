"""
Utility to fetch food images from Unsplash with fallback URLs.
https://unsplash.com/
Free stock photos with reliable CDN.
"""

import requests
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

# Map products to Unsplash search keywords
PRODUCT_SEARCH_KEYWORDS = {
    'Classic Chocolate Chip Cookies': 'chocolate chip cookies',
    'Double Chocolate Chip': 'chocolate cookie',
    'White Chocolate Chip': 'white chocolate cookie',
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

# Fallback URLs - Unsplash images (verified working)
FALLBACK_URLS = {
    'Classic Chocolate Chip Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Double Chocolate Chip': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'White Chocolate Chip': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Chocolate Cake Slice': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Vanilla Cake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Strawberry Cake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Chocolate Milkshake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Vanilla Milkshake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Strawberry Milkshake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Dark Chocolate Bar': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Milk Chocolate Bar': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Chocolate Truffles': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Almond Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Cranberry Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Walnut Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Oatmeal Raisin Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Oatmeal Honey Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Oatmeal Cranberry Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
}

# Category fallback URLs
CATEGORY_FALLBACKS = {
    'Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Cakes': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Chocolate': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Beverages': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
}


@lru_cache(maxsize=128)
def get_product_image_url(product_name, category_name=None):
    """
    Get image URL for a product.
    
    Priority:
    1. Return fallback URL from Unsplash (instant, no API call)
    2. Otherwise return default image URL
    """
    # Use Unsplash fallback URL
    if product_name in FALLBACK_URLS:
        return FALLBACK_URLS[product_name]
    
    # Fallback to category image
    if category_name and category_name in CATEGORY_FALLBACKS:
        return CATEGORY_FALLBACKS[category_name]
    
    # Default fallback
    return 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=800&q=80'


def get_category_image_url(category_name):
    """
    Get image URL for a category.
    
    Returns category-specific image or default.
    """
    if category_name in CATEGORY_FALLBACKS:
        return CATEGORY_FALLBACKS[category_name]
    
    # Default fallback
    return 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=800&q=80'
