#!/usr/bin/env python
"""Test ProductSerializer to verify mealdb image integration."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product
from products.serializers import ProductSerializer

try:
    # Get first product
    product = Product.objects.first()
    
    if product:
        print(f"Testing ProductSerializer...")
        serializer = ProductSerializer(product)
        data = serializer.data
        
        print(f"\n📦 Product: {data['name']}")
        print(f"📸 Image URL: {data['image']}")
        print(f"📂 Category: {data['category_name']}")
        
        # Verify it's a valid URL
        if data['image']:
            if 'themealdb' in data['image']:
                print("\n✅ SUCCESS! Returns Themealdb image URL!")
            elif data['image'].startswith('http'):
                print("\n✅ Returns valid HTTPS URL!")
            else:
                print(f"\n⚠️  Image appears to be a local path: {data['image']}")
        else:
            print("\n❌ ERROR: No image URL returned")
    else:
        print("❌ No products found in database. Please seed products first.")
        print("\nRun: python manage.py seed_products")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
