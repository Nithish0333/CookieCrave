"""
Utility to serve local product images from backend/media/product_images/
Downloaded images stored locally for faster loading.
"""

import os
from django.conf import settings

# Map products to local image filenames
PRODUCT_LOCAL_IMAGES = {
    'Classic Chocolate Chip Cookies': 'classic_chocolate_chip_cookies.jpg',
    'Double Chocolate Chip': 'double_chocolate_chip.jpg',
    'White Chocolate Chip': 'white_chocolate_chip.jpg',
    'Chocolate Cake Slice': 'chocolate_cake_slice.jpg',
    'Vanilla Cake': 'vanilla_cake.jpg',
    'Strawberry Cake': 'strawberry_cake.jpg',
    'Chocolate Milkshake': 'chocolate_milkshake.jpg',
    'Vanilla Milkshake': 'vanilla_milkshake.jpg',
    'Strawberry Milkshake': 'strawberry_milkshake.jpg',
    'Dark Chocolate Bar': 'dark_chocolate_bar.jpg',
    'Milk Chocolate Bar': 'milk_chocolate_bar.jpg',
    'Chocolate Truffles': 'chocolate_truffles.jpg',
    'Almond Cookies': 'almond_cookies.jpg',
    'Cranberry Cookies': 'cranberry_cookies.jpg',
    'Walnut Cookies': 'walnut_cookies.jpg',
    'Oatmeal Raisin Cookies': 'oatmeal_raisin_cookies.jpg',
    'Oatmeal Honey Cookies': 'oatmeal_honey_cookies.jpg',
    'Oatmeal Cranberry Cookies': 'oatmeal_cranberry_cookies.jpg',
}

# Fallback URLs for products that failed to download
FALLBACK_URLS = {
    'Dark Chocolate Bar': 'https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=800&q=80',
    'Milk Chocolate Bar': 'https://images.unsplash.com/photo-1599599810694-b5ac4dd33826?w=800&q=80',
    'Oatmeal Honey Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
    'Oatmeal Cranberry Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
}

# Category fallback URLs
CATEGORY_FALLBACKS = {
    'Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Cakes': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Chocolate': 'https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=800&q=80',
    'Beverages': 'https://images.unsplash.com/photo-1555939594-58d7cb561a1a?w=800&q=80',
}


def get_product_image_url(product_name, category_name=None):
    """
    Get image URL for a product (local or fallback).
    
    Priority:
    1. Local downloaded image from media/product_images/
    2. Fallback to Unsplash URL for failed downloads
    3. Category-based image
    4. Default image
    """
    # Check if local image exists
    if product_name in PRODUCT_LOCAL_IMAGES:
        filename = PRODUCT_LOCAL_IMAGES[product_name]
        # Use forward slashes for URLs (not OS-specific paths)
        local_path = f"{settings.MEDIA_URL}product_images/{filename}"
        
        # Verify file exists
        full_path = os.path.join(settings.MEDIA_ROOT, 'product_images', filename)
        if os.path.exists(full_path):
            return local_path
    
    # Use fallback URL if available
    if product_name in FALLBACK_URLS:
        return FALLBACK_URLS[product_name]
    
    # Use category image
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
