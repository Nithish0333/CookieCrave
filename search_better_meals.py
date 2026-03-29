#!/usr/bin/env python
"""
Better search for TheMealDB meals that match product names, ensuring uniqueness.
"""
import requests

MEALDB_API_BASE = "https://www.themealdb.com/api/json/v1/1"

# Manual mapping with best matches + fallbacks for items without exact matches
MANUAL_MAPPINGS = {
    'Classic Chocolate Chip Cookies': 'chocolate chip', 
    'Double Chocolate Chip': 'chocolate',
    'White Chocolate Chip': 'white chocolate',
    'Chocolate Cake Slice': 'chocolate cake',
    'Vanilla Cake': 'vanilla cake',
    'Strawberry Cake': 'strawberry cake',
    'Chocolate Milkshake': 'chocolate drink',
    'Vanilla Milkshake': 'vanilla dessert',
    'Strawberry Milkshake': 'strawberry drink',
    'Dark Chocolate Bar': 'dark chocolate',
    'Milk Chocolate Bar': 'milk chocolate',
    'Chocolate Truffles': 'truffle',
    'Almond Cookies': 'almond cookie',
    'Cranberry Cookies': 'cranberry',
    'Walnut Cookies': 'walnut',
    'Oatmeal Raisin Cookies': 'oatmeal raisin',
    'Oatmeal Honey Cookies': 'oatmeal',
    'Oatmeal Cranberry Cookies': 'oatmeal cranberry',
}

print("\n🔍 SEARCHING WITH BETTER MATCHING TERMS\n")
print("=" * 90)

meal_mapping = {}
used_ids = set()

for product, search_term in MANUAL_MAPPINGS.items():
    print(f"\n📦 {product}")
    print(f"   Search term: '{search_term}'")
    
    try:
        url = f"{MEALDB_API_BASE}/search.php?s={search_term}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('meals'):
            # Find first meal not yet used
            selected_meal = None
            for meal in data['meals']:
                meal_id = meal['idMeal']
                meal_name = meal['strMeal']
                
                if meal_id not in used_ids:
                    selected_meal = (meal_id, meal_name)
                    break
            
            if selected_meal:
                meal_id, meal_name = selected_meal
                meal_mapping[product] = meal_id
                used_ids.add(meal_id)
                print(f"   ✅ {meal_name} (ID: {meal_id})")
            else:
                # If all are used, take first anyway (will handle later)
                meal_id = data['meals'][0]['idMeal']
                meal_name = data['meals'][0]['strMeal']
                meal_mapping[product] = meal_id
                print(f"   ⚠️  {meal_name} (ID: {meal_id}) [already used]")
        else:
            print(f"   ❌ No match found")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 90)
print("\nFINAL MAPPING (18 products, {} unique meals):\n".format(len(used_ids)))
print("PRODUCT_SPECIFIC_IDS = {")
for product, meal_id in meal_mapping.items():
    print(f"    '{product}': {meal_id},")
print("}")

# Count duplicates
duplicate_ids = {}
for product, meal_id in meal_mapping.items():
    if meal_id not in duplicate_ids:
        duplicate_ids[meal_id] = []
    duplicate_ids[meal_id].append(product)

dupes = {mid: prods for mid, prods in duplicate_ids.items() if len(prods) > 1}
if dupes:
    print(f"\n⚠️  DUPLICATE MEAL IDS:")
    for meal_id, products in dupes.items():
        print(f"   ID {meal_id}: {', '.join(products)}")
else:
    print(f"\n✅ No duplicate meal IDs!")
