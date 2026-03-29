#!/usr/bin/env python
import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product
from products.serializers import ProductSerializer

print("=" * 80)
print("FINAL IMAGE SETUP SUMMARY")
print("=" * 80)

products = Product.objects.all()
local_count = 0
fallback_count = 0

print(f"\n📊 Total Products: {len(products)}")
print("\n🖼️  Image Status:")
print("-" * 80)

for product in products:
    serializer = ProductSerializer(product)
    image_url = serializer.data.get('image')
    
    if '/media/' in image_url:
        status = "✅ LOCAL"
        local_count += 1
        filename = image_url.split('/')[-1]
        print(f"{product.name:40} → {status} ({filename})")
    else:
        status = "🌐 EXTERNAL"
        fallback_count += 1
        print(f"{product.name:40} → {status}")

print("\n" + "=" * 80)
print("SUMMARY:")
print("=" * 80)
print(f"✅ Local Images:    {local_count}/{len(products)}")
print(f"🌐 Fallback URLs:   {fallback_count}/{len(products)}")
print(f"\n📁 Images Location: {os.path.abspath('media/product_images')}")
print(f"🔗 API Endpoint:    http://localhost:8000/api/products/")
print(f"🌐 Media URL:       http://localhost:8000/media/product_images/")
print("\n" + "=" * 80)
print("✅ SETUP COMPLETE!")
print("=" * 80)
