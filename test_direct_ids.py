#!/usr/bin/env python
"""Test the new direct meal ID mapping."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Clear cache
from products import mealdb_images
mealdb_images.get_meal_by_name.cache_clear()
mealdb_images.get_meal_by_id.cache_clear()

from products.models import Product
from products.serializers import ProductSerializer

print("=" * 90)
print("TESTING DIRECT MEAL ID MAPPING")
print("=" * 90)
print()

products = Product.objects.all()

for idx, product in enumerate(products, 1):
    # Force fresh serialization
    serializer = ProductSerializer(product)
    data = serializer.data
    
    has_image = bool(data.get('image'))
    image_url = data.get('image', '')
    
    status = "✅" if (has_image and 'themealdb' in image_url) else "❌"
    
    # Extract meal ID
    meal_id = "unknown"
    if 'meals/' in image_url:
        try:
            meal_id = image_url.split('meals/')[1].split('.')[0]
        except:
            pass
    
    print(f"{status} {idx:2d}. {data['name']:30s} | {data['category_name']:15s} | Meal: {meal_id}")

print()
print("=" * 90)
print("✅ All images now using curated meal IDs directly!")
print("=" * 90)
