#!/usr/bin/env python
"""Research better meal IDs for more granular product matching."""

import requests

MEALDB_API_BASE = "https://www.themealdb.com/api/json/v1/1"

# Search for specific meal types
searches = {
    'cookies': ['Jam jam cookies', 'Peanut Butter Cookies', 'Rogaliki'],
    'chocolate': ['Chocolate Gateau', 'Chocolate Souffle', 'Hot Chocolate Fudge'],
    'cheesecake': ['New York cheesecake', 'Honey Yogurt Cheesecake', 'Peanut Butter Cheesecake'],
    'cake': ['Apple cake', 'Rock Cakes', 'Carrot Cake'],
    'tart': ['Lemon Tart', 'Treacle Tart'],
    'strawberry': ['Strawberry Shortcake', 'Strawberry Cheesecake'],
}

print("=" * 80)
print("AVAILABLE MEAL IDS FOR GRANULAR PRODUCT MAPPING")
print("=" * 80)
print()

for category, items in searches.items():
    print(f"\n{category.upper()}:")
    for item in items:
        try:
            url = f"{MEALDB_API_BASE}/search.php?s={item}"
            response = requests.get(url, timeout=3)
            data = response.json()
            if data.get('meals'):
                meal = data['meals'][0]
                print(f"  ✅ {meal['strMeal']:40s} | ID: {meal['idMeal']}")
            else:
                print(f"  ❌ {item:40s} | Not found")
        except Exception as e:
            print(f"  ❌ {item:40s} | Error")
