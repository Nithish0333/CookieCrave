#!/usr/bin/env python
import os
import django
import sys

backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

print("Clearing existing image URLs to enable unique Unsplash API images...")
print("=" * 80)

cleared_count = 0
for product in Product.objects.all():
    if product.image and str(product.image).startswith('http'):
        product.image = None  # Clear the stored URL
        product.save()
        cleared_count += 1
        print(f"✅ Cleared image for: {product.name}")

print("=" * 80)
print(f"\n📊 SUMMARY: Cleared {cleared_count} product images")
print("   - Products will now get unique images from Unsplash API")
print("   - Images will be fetched based on product names and categories")
