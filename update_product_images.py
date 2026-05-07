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
from products.unsplash_working_images import get_product_image_url

print("Updating all products with verified working Unsplash URLs...")
print("=" * 80)

updated_count = 0
for product in Product.objects.all():
    # Get the verified working URL for this product
    verified_url = get_product_image_url(product.name, product.category.name if product.category else None)
    
    # Update the product's image field
    if product.image != verified_url:
        product.image = verified_url
        product.save()
        updated_count += 1
        print(f"✅ Updated: {product.name}")
        print(f"   Old: {product.image}")
        print(f"   New: {verified_url}")

print("=" * 80)
print(f"\n📊 SUMMARY: Updated {updated_count} products with verified Unsplash URLs")
