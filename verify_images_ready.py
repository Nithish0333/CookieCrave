#!/usr/bin/env python
"""Verify that product images show up in the next 10 items from the API."""

import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product
from products.serializers import ProductSerializer

products = Product.objects.all()[:10]

print("=" * 80)
print("PRODUCT IMAGE VERIFICATION")
print("=" * 80)
print()

image_count = 0
for idx, product in enumerate(products, 1):
    serializer = ProductSerializer(product)
    data = serializer.data
    
    has_image = bool(data.get('image'))
    is_mealdb = 'themealdb' in str(data.get('image', ''))
    
    status = "✅" if (has_image and is_mealdb) else "❌"
    
    print(f"{status} Product {idx}: {data['name']}")
    print(f"   Category: {data['category_name']}")
    print(f"   Image: {data.get('image', 'None')[:80]}...")
    print()
    
    if has_image and is_mealdb:
        image_count += 1

print("=" * 80)
print(f"SUMMARY: {image_count}/{len(products)} products have mealdb images")
print("=" * 80)

if image_count == len(products):
    print("\n✅ SUCCESS! All products are ready to display images!")
    print("📱 Go to http://localhost:5174 to see the marketplace with images")
else:
    print(f"\n⚠️  Only {image_count} of {len(products)} products have images")
