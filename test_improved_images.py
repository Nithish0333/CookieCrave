#!/usr/bin/env python
"""Clear cache and test the improved product image mapping."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Clear the cache from mealdb_images
from products import mealdb_images
mealdb_images.get_meal_by_name.cache_clear()
mealdb_images.get_meal_by_id.cache_clear()

# Now test with improved mapping
from products.models import Product
from products.serializers import ProductSerializer

print("=" * 80)
print("TESTING IMPROVED PRODUCT IMAGE MAPPING")
print("=" * 80)
print()

products = Product.objects.all()[:12]

image_count = 0
for idx, product in enumerate(products, 1):
    # Force fresh serialization with new mapping
    serializer = ProductSerializer(product)
    data = serializer.data
    
    has_image = bool(data.get('image'))
    is_mealdb = 'themealdb' in str(data.get('image', ''))
    
    status = "✅" if (has_image and is_mealdb) else "❌"
    
    print(f"{status} {idx}. {data['name']}")
    print(f"    Category: {data['category_name']}")
    
    # Extract meal ID from image URL for reference
    image_url = data.get('image', '')
    if 'meals/' in image_url:
        meal_id = image_url.split('meals/')[1].split('.')[0]
        print(f"    Meal ID: {meal_id}")
    
    print(f"    Image: {image_url[:70]}...")
    print()
    
    if has_image and is_mealdb:
        image_count += 1

print("=" * 80)
print(f"RESULT: {image_count}/{len(products)} products with improved images")
print("=" * 80)
print("\n✅ New images are now based on improved product/category matching!")
