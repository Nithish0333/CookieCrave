#!/usr/bin/env python
import os
import sys
import django
import requests

# Setup Django
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product
from products.serializers import ProductSerializer

print("=" * 80)
print("CHECKING IMAGE URL STATUS")
print("=" * 80)

# Check backend API
print("\n1. Testing Backend API Connectivity...")
try:
    response = requests.get('http://localhost:8000/api/products/', timeout=5)
    print(f"   ✅ Backend API: Status {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data:
            first_product = data[0]
            print(f"   ✅ API Response: {len(data)} products found")
            print(f"   📦 First Product: {first_product.get('name')}")
            print(f"   🖼️  Image URL: {first_product.get('image')}")
except Exception as e:
    print(f"   ❌ Backend API Error: {e}")

# Check database serialization
print("\n2. Checking Database + Serializer...")
try:
    products = Product.objects.all()[:3]
    for product in products:
        serializer = ProductSerializer(product)
        data = serializer.data
        print(f"\n   📦 {product.name}")
        print(f"      Image URL: {data.get('image')}")
        
        # Check if URL is valid
        if data.get('image'):
            if data['image'].startswith('http'):
                print(f"      ✅ URL format valid")
            else:
                print(f"      ❌ URL format INVALID - should start with http")
except Exception as e:
    print(f"   ❌ Serializer Error: {e}")

# Check if image URLs are accessible
print("\n3. Testing Image URL Accessibility...")
try:
    product = Product.objects.first()
    if product:
        serializer = ProductSerializer(product)
        image_url = serializer.data.get('image')
        if image_url:
            print(f"   Testing: {image_url[:70]}...")
            img_response = requests.head(image_url, timeout=5)
            if img_response.status_code == 200:
                print(f"   ✅ Image accessible (HTTP {img_response.status_code})")
            else:
                print(f"   ❌ Image not accessible (HTTP {img_response.status_code})")
        else:
            print(f"   ❌ No image URL returned from serializer")
except Exception as e:
    print(f"   ⚠️  Could not test image accessibility: {e}")

print("\n" + "=" * 80)
