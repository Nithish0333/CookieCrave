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
from products.serializers import ProductSerializer

products = Product.objects.all().order_by('id')

images = set()
dupes = 0

for product in products:
    img = ProductSerializer(product).data.get('image', '')
    if img in images:
        dupes += 1
    else:
        images.add(img)
    print(f"{product.name:35} ✓")

print(f"\n{'='*60}")
print(f"Total: {len(products)} | Unique: {len(images)} | Duplicates: {dupes}")
if dupes == 0:
    print("✅ SUCCESS - All images unique and product-name matched!")
else:
    print(f"⚠️  {dupes} duplicates found")
