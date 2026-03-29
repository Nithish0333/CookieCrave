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

print("Checking product image fields vs fallback URLs...")
print("=" * 80)

for product in Product.objects.all()[:5]:
    print(f"\nProduct: {product.name}")
    print(f"  Database image field: {repr(product.image)}")
    print(f"  Fallback URL: {get_product_image_url(product.name, product.category.name if product.category else None)}")
    
    # Check if the product has an actual image file
    if product.image:
        print(f"  ✅ Has image file: {product.image.name}")
    else:
        print(f"  ❌ No image file in database")

print("=" * 80)
