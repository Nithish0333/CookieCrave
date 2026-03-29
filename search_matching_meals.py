#!/usr/bin/env python
"""
Search TheMealDB for actual meals that match product names.
"""
import requests

MEALDB_API_BASE = "https://www.themealdb.com/api/json/v1/1"

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

# Search terms to try for each product
search_terms = {
    'Classic Chocolate Chip Cookies': ['cookies', 'chocolate chip'],
    'Double Chocolate Chip': ['chocolate', 'brownies'],
    'White Chocolate Chip': ['chocolate', 'white'],
    'Chocolate Cake Slice': ['chocolate cake', 'cake'],
    'Vanilla Cake': ['vanilla cake', 'cake'],
    'Strawberry Cake': ['strawberry', 'cake'],
    'Chocolate Milkshake': ['chocolate milkshake', 'milkshake'],
    'Vanilla Milkshake': ['vanilla milkshake', 'milkshake'],
    'Strawberry Milkshake': ['strawberry milkshake', 'smoothie'],
    'Dark Chocolate Bar': ['chocolate', 'dessert'],
    'Milk Chocolate Bar': ['chocolate', 'dessert'],
    'Chocolate Truffles': ['chocolate', 'truffle'],
    'Almond Cookies': ['almond', 'cookie'],
    'Cranberry Cookies': ['cranberry', 'cookie'],
    'Walnut Cookies': ['walnut', 'cookie'],
    'Oatmeal Raisin Cookies': ['oatmeal', 'raisin'],
    'Oatmeal Honey Cookies': ['oatmeal', 'honey'],
    'Oatmeal Cranberry Cookies': ['oatmeal', 'cranberry'],
}

print("\n🔍 SEARCHING MEALDB FOR MATCHING MEALS\n")
print("=" * 80)

meal_mapping = {}

for product in products:
    print(f"\n📦 {product}")
    found = False
    
    for search_term in search_terms.get(product, [product.split()[0]]):
        if found:
            break
            
        try:
            url = f"{MEALDB_API_BASE}/search.php?s={search_term}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get('meals'):
                # Take first matching meal
                meal = data['meals'][0]
                meal_id = meal['idMeal']
                meal_name = meal['strMeal']
                
                meal_mapping[product] = meal_id
                print(f"   ✅ Found: {meal_name} (ID: {meal_id})")
                found = True
        except Exception as e:
            print(f"   ⚠️  Error searching '{search_term}': {e}")
    
    if not found:
        print(f"   ❌ No match found")

print("\n" + "=" * 80)
print("\nPYTHON DICT (Copy this to mealdb_images.py):\n")
print("PRODUCT_SPECIFIC_IDS = {")
for product, meal_id in meal_mapping.items():
    # Fetch meal name for reference
    try:
        response = requests.get(f"{MEALDB_API_BASE}/lookup.php?i={meal_id}", timeout=5)
        meal_data = response.json()
        if meal_data.get('meals'):
            meal_name = meal_data['meals'][0].get('strMeal', 'Unknown')
            print(f"    '{product}': {meal_id},  # {meal_name}")
        else:
            print(f"    '{product}': {meal_id},")
    except:
        print(f"    '{product}': {meal_id},")

print("}")
