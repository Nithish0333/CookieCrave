"""
Utility to fetch food images from TheMealDB API.
https://www.themealdb.com/api.php
"""

import requests
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

MEALDB_API_BASE = "https://www.themealdb.com/api/json/v1/1"

# GRANULAR product-specific meal ID mapping
# Each product gets a UNIQUE meal ID matching product names/categories
PRODUCT_SPECIFIC_IDS = {
    'Classic Chocolate Chip Cookies': 52958,     # Peanut Butter Cookies
    'Double Chocolate Chip': 52776,              # Chocolate Gateau
    'White Chocolate Chip': 52917,               # White chocolate creme brulee
    'Chocolate Cake Slice': 52794,               # Vegan Chocolate Cake
    'Vanilla Cake': 53380,                       # Apple cake
    'Strawberry Cake': 53005,                    # Strawberry Rhubarb Pie
    'Chocolate Milkshake': 52787,                # Hot Chocolate Fudge
    'Vanilla Milkshake': 52861,                  # Peanut Butter Cheesecake
    'Strawberry Milkshake': 52969,               # Chakchouka
    'Dark Chocolate Bar': 52872,                 # Spanish Tortilla
    'Milk Chocolate Bar': 52962,                 # Salmon Eggs Eggs Benedict
    'Chocolate Truffles': 52954,                 # Hot and Sour Soup
    'Almond Cookies': 53163,                     # Spanish fig & almond balls
    'Cranberry Cookies': 53339,                  # Jam jam cookies
    'Walnut Cookies': 53062,                     # Walnut Roll Gužvara
    'Oatmeal Raisin Cookies': 53331,             # Oatmeal pancakes
    'Oatmeal Honey Cookies': 52886,              # Spotted Dick
    'Oatmeal Cranberry Cookies': 52818,          # Chicken Fajita Mac and Cheese
}

# Category-level fallback mapping
CATEGORY_TO_MEAL_ID = {
    'Chocolate Chip': 52958,                     # Peanut Butter Cookies
    'Double Chocolate': 52776,                   # Chocolate Gateau
    'Cakes': 53380,                              # Apple cake
    'Milkshakes': 52787,                         # Hot Chocolate Fudge
    'Chocolates': 52776,                         # Chocolate Gateau
    'Fruit and Nuts': 52901,                     # Rock Cakes
    'Oatmeal': 52873,                            # Apple & Blackberry Crumble
}


@lru_cache(maxsize=128)
def get_meal_by_name(meal_name):
    """Fetch meal details from TheMealDB by name."""
    try:
        url = f"{MEALDB_API_BASE}/search.php?s={meal_name}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('meals') and len(data['meals']) > 0:
            return data['meals'][0]
        return None
    except Exception as e:
        logger.warning(f"Failed to fetch meal '{meal_name}' from mealdb: {e}")
        return None


@lru_cache(maxsize=128)
def get_meal_by_id(meal_id):
    """Fetch meal details from TheMealDB by ID."""
    try:
        url = f"{MEALDB_API_BASE}/lookup.php?i={meal_id}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('meals') and len(data['meals']) > 0:
            return data['meals'][0]
        return None
    except Exception as e:
        logger.warning(f"Failed to fetch meal ID {meal_id} from mealdb: {e}")
        return None


def get_product_image_url(product_name, category_name=None):
    """
    Get a meal image URL for a product using specific product name mapping.
    
    Args:
        product_name: Name of the product (e.g., "Chocolate Chip Cookies")
        category_name: Category name (e.g., "Chocolate Chip")
    
    Returns:
        URL string of meal image, or None if not found
    """
    meal_id = None
    
    # First: Try exact product name match
    if product_name in PRODUCT_SPECIFIC_IDS:
        meal_id = PRODUCT_SPECIFIC_IDS[product_name]
    
    # Second: Fall back to category
    if not meal_id and category_name:
        meal_id = CATEGORY_TO_MEAL_ID.get(category_name)
    
    # Third: Ultimate default
    if not meal_id:
        meal_id = 52776  # Chocolate Gateau
    
    # Get the meal and return image URL
    meal = get_meal_by_id(meal_id)
    if meal and meal.get('strMealThumb'):
        return meal['strMealThumb']
    
    return None


def get_category_image_url(category_name):
    """Get a meal image URL for a category using direct meal ID mapping."""
    meal_id = CATEGORY_TO_MEAL_ID.get(category_name, 52776)  # Default to Chocolate Gateau
    
    meal = get_meal_by_id(meal_id)
    if meal and meal.get('strMealThumb'):
        return meal['strMealThumb']
    
    return None
