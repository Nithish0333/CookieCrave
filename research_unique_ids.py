#!/usr/bin/env python
"""
Research and find unique meal IDs for all 18 products.
"""
import requests

MEALDB_API_BASE = "https://www.themealdb.com/api/json/v1/1"

# These are actual meal IDs we can query directly
UNIQUE_MEAL_IDS = [
    52958,  # Peanut Butter Cookies
    52905,  # Chocolate Souffle
    52858,  # New York cheesecake
    52776,  # Chocolate Gateau
    52787,  # Hot Chocolate Fudge
    52872,  # Chocolate Gateau variant
    52901,  # Rock Cakes
    52861,  # Peanut Butter Cheesecake
    52960,  # Bread and Butter Pudding
    52873,  # Apple & Blackberry Crumble
    53380,  # Apple cake
    52954,  # Carrot Cake
    52957,  # Strawberry Shortcake
    52969,  # Banana Cinnamon Pancakes
    52975,  # Cherry Cheesecake
    52886,  # Tiramisu
    52917,  # Chocolate Dipped Strawberries
    52928,  # Croissants
]

products = [
    'Classic Chocolate Chip Cookies',
    'Double Chocolate Chip',
    'White Chocolate Chip',
    'Chocolate Cake Slice',
    'Vanilla Cake',
    'Strawberry Cake',
    'Chocolate Milkshake',
    'Vanilla Milkshake',
    'Strawberry Milkshake',
    'Dark Chocolate Bar',
    'Milk Chocolate Bar',
    'Chocolate Truffles',
    'Almond Cookies',
    'Cranberry Cookies',
    'Walnut Cookies',
    'Oatmeal Raisin Cookies',
    'Oatmeal Honey Cookies',
    'Oatmeal Cranberry Cookies',
]

print("UNIQUE MEAL IDS FOUND:")
print("=" * 60)

# Map each product to a unique meal ID
mapping = {}
for i, product in enumerate(products):
    meal_id = UNIQUE_MEAL_IDS[i]
    mapping[product] = meal_id
    
    # Try to fetch the meal to verify it exists
    try:
        response = requests.get(f"{MEALDB_API_BASE}/lookup.php?i={meal_id}", timeout=5)
        meal_data = response.json()
        if meal_data.get('meals'):
            meal_name = meal_data['meals'][0].get('strMeal', 'Unknown')
            print(f"{i+1:2}. {product:35} → {meal_id:10} ({meal_name})")
        else:
            print(f"{i+1:2}. {product:35} → {meal_id:10} (NOT FOUND)")
    except Exception as e:
        print(f"{i+1:2}. {product:35} → {meal_id:10} (ERROR: {e})")

print("\n" + "=" * 60)
print("\nPYTHON DICT FORMAT:")
print("PRODUCT_SPECIFIC_IDS = {")
for product, meal_id in mapping.items():
    print(f"    '{product}': {meal_id},")
print("}")
