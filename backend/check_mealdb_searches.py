#!/usr/bin/env python
"""Check what meals are actually being returned by mealdb search."""

import requests

MEALDB_API_BASE = "https://www.themealdb.com/api/json/v1/1"

search_terms = ['cookie', 'cake', 'chocolate', 'milkshake', 'dessert', 'cheesecake']

print("=" * 80)
print("CHECKING ACTUAL MEALDB SEARCH RESULTS")
print("=" * 80)
print()

for term in search_terms:
    try:
        url = f"{MEALDB_API_BASE}/search.php?s={term}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get('meals'):
            meals = data['meals'][:3]  # Get first 3 results
            print(f"🔍 Search: '{term}'")
            print(f"   Found {len(data['meals'])} results")
            for idx, meal in enumerate(meals, 1):
                print(f"   {idx}. {meal['strMeal']} (ID: {meal['idMeal']})")
            print()
        else:
            print(f"❌ Search: '{term}' - No results found")
            print()
    except Exception as e:
        print(f"❌ Error searching '{term}': {e}")
        print()

print("=" * 80)
print("RECOMMENDATION: Use specific meal IDs instead of search terms")
print("=" * 80)
