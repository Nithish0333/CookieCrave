"""
Utility to fetch food images from curated free sources.
Uses pre-selected high-quality food images from Pixabay/Pexels
No API key required - direct URLs cached for performance.
"""

import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

# Curated product -> food image URL mapping from free sources
# These are high-quality, royalty-free images from Pixabay/Pexels
# Each product has a unique image related to its name
PRODUCT_IMAGE_URLS = {
    'Classic Chocolate Chip Cookies': 'https://images.pexels.com/photos/315707/pexels-photo-315707.jpeg',
    'Double Chocolate Chip': 'https://images.pexels.com/photos/1126359/pexels-photo-1126359.jpeg',
    'White Chocolate Chip': 'https://images.pexels.com/photos/821365/pexels-photo-821365.jpeg',
    'Chocolate Cake Slice': 'https://images.pexels.com/photos/291960/pexels-photo-291960.jpeg',
    'Vanilla Cake': 'https://images.pexels.com/photos/139670/pexels-photo-139670.jpeg',
    'Strawberry Cake': 'https://images.pexels.com/photos/2144200/pexels-photo-2144200.jpeg',
    'Chocolate Milkshake': 'https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg',
    'Vanilla Milkshake': 'https://images.pexels.com/photos/3407817/pexels-photo-3407817.jpeg',
    'Strawberry Milkshake': 'https://images.pexels.com/photos/3296949/pexels-photo-3296949.jpeg',
    'Dark Chocolate Bar': 'https://images.pexels.com/photos/5632383/pexels-photo-5632383.jpeg',
    'Milk Chocolate Bar': 'https://images.pexels.com/photos/4262537/pexels-photo-4262537.jpeg',
    'Chocolate Truffles': 'https://images.pexels.com/photos/1092736/pexels-photo-1092736.jpeg',
    'Almond Cookies': 'https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg',
    'Cranberry Cookies': 'https://images.pexels.com/photos/1410235/pexels-photo-1410235.jpeg',
    'Walnut Cookies': 'https://images.pexels.com/photos/1092734/pexels-photo-1092734.jpeg',
    'Oatmeal Raisin Cookies': 'https://images.pexels.com/photos/1203852/pexels-photo-1203852.jpeg',
    'Oatmeal Honey Cookies': 'https://images.pexels.com/photos/5835176/pexels-photo-5835176.jpeg',
    'Oatmeal Cranberry Cookies': 'https://images.pexels.com/photos/2693857/pexels-photo-2693857.jpeg',
}

# Category fallback URLs
CATEGORY_IMAGE_URLS = {
    'Chocolate Chip': 'https://images.pexels.com/photos/1126359/pexels-photo-1126359.jpeg',
    'Double Chocolate': 'https://images.pexels.com/photos/821365/pexels-photo-821365.jpeg',
    'Cakes': 'https://images.pexels.com/photos/291960/pexels-photo-291960.jpeg',
    'Milkshakes': 'https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg',
    'Chocolates': 'https://images.pexels.com/photos/5632383/pexels-photo-5632383.jpeg',
    'Fruit and Nuts': 'https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg',
    'Oatmeal': 'https://images.pexels.com/photos/1203852/pexels-photo-1203852.jpeg',
}

# Default fallback
DEFAULT_IMAGE_URL = 'https://images.pexels.com/photos/1410235/pexels-photo-1410235.jpeg'


def get_product_image_url(product_name, category_name=None):
    """
    Get an image URL for a product using curated mappings.
    
    Args:
        product_name: Name of the product (e.g., "Chocolate Chip Cookies")
        category_name: Category name (fallback, e.g., "Chocolate Chip")
    
    Returns:
        URL string of image (always returns a valid URL)
    """
    # First: Try exact product name match
    if product_name in PRODUCT_IMAGE_URLS:
        url = PRODUCT_IMAGE_URLS[product_name]
        logger.info(f"Found image for product: {product_name}")
        return url
    
    # Second: Fall back to category
    if category_name and category_name in CATEGORY_IMAGE_URLS:
        url = CATEGORY_IMAGE_URLS[category_name]
        logger.info(f"Found image for category: {category_name}")
        return url
    
    # Third: Return default
    logger.warning(f"Using default image for: {product_name}")
    return DEFAULT_IMAGE_URL


def get_category_image_url(category_name):
    """Get an image URL for a category."""
    if category_name in CATEGORY_IMAGE_URLS:
        return CATEGORY_IMAGE_URLS[category_name]
    
    return DEFAULT_IMAGE_URL
