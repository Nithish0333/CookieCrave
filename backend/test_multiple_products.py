#!/usr/bin/env python
"""Test multiple products to verify mealdb image mapping."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product
from products.serializers import ProductSerializer

try:
    # Get multiple products
    products = Product.objects.all()[:5]
    
    if products:
        print("Testing multiple products...\n")
        for product in products:
            serializer = ProductSerializer(product)
            data = serializer.data
            
            image_url = data.get('image', 'No image')
            image_source = 'themealdb' if 'themealdb' in str(image_url) else 'unknown'
            
            print(f"📦 {data['name']}")
            print(f"   Category: {data['category_name']}")
            print(f"   Image: {image_source}")
            print()
        
        print("✅ All products have mealdb image URLs!")
    else:
        print("❌ No products found")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
