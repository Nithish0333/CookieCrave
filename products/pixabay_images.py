"""
Utility to fetch food images from Pixabay.
https://pixabay.com/
High-quality, royalty-free images curated for each product.
"""

import logging

logger = logging.getLogger(__name__)

# Curated product -> Pixabay image URL mapping
# Each product has a unique, semantically-related image from Pixabay
PRODUCT_IMAGE_URLS = {
    'Classic Chocolate Chip Cookies': 'https://cdn.pixabay.com/photo/2015/03/26/09/47/chocolate-690353_1280.jpg',
    'Double Chocolate Chip': 'https://cdn.pixabay.com/photo/2018/04/03/14/45/chocolate-3285828_1280.jpg',
    'White Chocolate Chip': 'https://cdn.pixabay.com/photo/2019/09/29/08/21/white-chocolate-4510993_1280.jpg',
    'Chocolate Cake Slice': 'https://cdn.pixabay.com/photo/2016/11/22/20/09/chocolate-cake-1850011_1280.jpg',
    'Vanilla Cake': 'https://cdn.pixabay.com/photo/2015/12/09/17/11/cake-1084541_1280.jpg',
    'Strawberry Cake': 'https://cdn.pixabay.com/photo/2019/01/14/10/34/strawberry-cake-3933100_1280.jpg',
    'Chocolate Milkshake': 'https://cdn.pixabay.com/photo/2019/01/28/22/40/chocolate-shake-3962402_1280.jpg',
    'Vanilla Milkshake': 'https://cdn.pixabay.com/photo/2019/08/30/08/20/milkshake-4442521_1280.jpg',
    'Strawberry Milkshake': 'https://cdn.pixabay.com/photo/2019/05/05/10/27/strawberry-shake-4181904_1280.jpg',
    'Dark Chocolate Bar': 'https://cdn.pixabay.com/photo/2014/10/01/10/25/chocolate-472720_1280.jpg',
    'Milk Chocolate Bar': 'https://cdn.pixabay.com/photo/2020/03/24/14/45/chocolate-4963388_1280.jpg',
    'Chocolate Truffles': 'https://cdn.pixabay.com/photo/2018/02/28/23/34/chocolate-truffles-3189516_1280.jpg',
    'Almond Cookies': 'https://cdn.pixabay.com/photo/2017/10/10/18/43/biscuit-2837849_1280.jpg',
    'Cranberry Cookies': 'https://cdn.pixabay.com/photo/2018/04/12/00/44/cookies-3309046_1280.jpg',
    'Walnut Cookies': 'https://cdn.pixabay.com/photo/2017/07/03/18/53/cookies-2469005_1280.jpg',
    'Oatmeal Raisin Cookies': 'https://cdn.pixabay.com/photo/2019/07/08/10/03/biscuits-4325486_1280.jpg',
    'Oatmeal Honey Cookies': 'https://cdn.pixabay.com/photo/2019/09/17/19/01/biscuit-4486093_1280.jpg',
    'Oatmeal Cranberry Cookies': 'https://cdn.pixabay.com/photo/2018/08/29/20/03/cookies-3639621_1280.jpg',
}

# Category fallback URLs
CATEGORY_IMAGE_URLS = {
    'Chocolate Chip': 'https://cdn.pixabay.com/photo/2015/03/26/09/47/chocolate-690353_1280.jpg',
    'Double Chocolate': 'https://cdn.pixabay.com/photo/2018/04/03/14/45/chocolate-3285828_1280.jpg',
    'Cakes': 'https://cdn.pixabay.com/photo/2016/11/22/20/09/chocolate-cake-1850011_1280.jpg',
    'Milkshakes': 'https://cdn.pixabay.com/photo/2019/01/28/22/40/chocolate-shake-3962402_1280.jpg',
    'Chocolates': 'https://cdn.pixabay.com/photo/2014/10/01/10/25/chocolate-472720_1280.jpg',
    'Fruit and Nuts': 'https://cdn.pixabay.com/photo/2017/10/10/18/43/biscuit-2837849_1280.jpg',
    'Oatmeal': 'https://cdn.pixabay.com/photo/2019/07/08/10/03/biscuits-4325486_1280.jpg',
}

# Default fallback
DEFAULT_IMAGE_URL = 'https://cdn.pixabay.com/photo/2015/03/26/09/47/chocolate-690353_1280.jpg'


def get_product_image_url(product_name, category_name=None):
    """
    Get a Pixabay image URL for a product using curated mappings.
    
    Args:
        product_name: Name of the product (e.g., "Chocolate Chip Cookies")
        category_name: Category name (fallback, e.g., "Chocolate Chip")
    
    Returns:
        URL string of image (always returns a valid URL)
    """
    # First: Try exact product name match
    if product_name in PRODUCT_IMAGE_URLS:
        url = PRODUCT_IMAGE_URLS[product_name]
        logger.info(f"Found Pixabay image for product: {product_name}")
        return url
    
    # Second: Fall back to category
    if category_name and category_name in CATEGORY_IMAGE_URLS:
        url = CATEGORY_IMAGE_URLS[category_name]
        logger.info(f"Found Pixabay image for category: {category_name}")
        return url
    
    # Third: Return default
    logger.warning(f"Using default Pixabay image for: {product_name}")
    return DEFAULT_IMAGE_URL


def get_category_image_url(category_name):
    """Get a Pixabay image URL for a category."""
    if category_name in CATEGORY_IMAGE_URLS:
        return CATEGORY_IMAGE_URLS[category_name]
    
    return DEFAULT_IMAGE_URL
