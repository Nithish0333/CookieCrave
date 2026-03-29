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
print("DIAGNOSING IMAGE DISPLAY ISSUE")
print("=" * 80)

# Test 1: Check API connectivity
print("\n1️⃣ Testing API Connectivity...")
try:
    response = requests.get('http://localhost:8000/api/products/', timeout=5)
    print(f"   ✅ Backend API: Status {response.status_code}")
    data = response.json()
    print(f"   ✅ Products returned: {len(data)}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Check image URLs in API response
print("\n2️⃣ Checking Image URLs in API Response...")
first_product = data[0]
image_url = first_product.get('image')
print(f"   📦 Product: {first_product['name']}")
print(f"   🖼️  Raw URL: {image_url}")

# Test 3: Check if URL is accessible
if image_url:
    print(f"\n3️⃣ Testing Image URL Accessibility...")
    
    # For local URLs, make it absolute
    if image_url.startswith('/'):
        test_url = f"http://localhost:8000{image_url}"
        print(f"   🔗 Testing: {test_url}")
    else:
        test_url = image_url
        print(f"   🔗 Testing: {test_url}")
    
    try:
        img_response = requests.get(test_url, timeout=10)
        print(f"   Status: HTTP {img_response.status_code}")
        
        if img_response.status_code == 200:
            print(f"   ✅ Image is accessible")
            print(f"   Content-Type: {img_response.headers.get('content-type')}")
            print(f"   Size: {len(img_response.content) / 1024:.1f}KB")
        else:
            print(f"   ❌ Image returned error: HTTP {img_response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Test 4: Check file system
print(f"\n4️⃣ Checking File System...")
media_dir = os.path.abspath(os.path.join(backend_path, 'media', 'product_images'))
if os.path.exists(media_dir):
    files = os.listdir(media_dir)
    print(f"   ✅ Media directory exists: {media_dir}")
    print(f"   📁 Files found: {len(files)}")
    if files:
        print(f"   Sample files:")
        for f in files[:3]:
            filepath = os.path.join(media_dir, f)
            size = os.path.getsize(filepath) / 1024
            print(f"      - {f} ({size:.1f}KB)")
else:
    print(f"   ❌ Media directory not found: {media_dir}")

# Test 5: Check serializer
print(f"\n5️⃣ Checking Serializer Output...")
product = Product.objects.first()
if product:
    serializer = ProductSerializer(product)
    data = serializer.data
    img = data.get('image')
    print(f"   📦 Product: {product.name}")
    print(f"   🖼️  Image from serializer: {img}")
    
    # Check if file exists on disk
    if img and '/media/' in img:
        full_path = os.path.join(backend_path, 'media', img.replace('/media/', ''))
        if os.path.exists(full_path):
            print(f"   ✅ File exists on disk")
        else:
            print(f"   ❌ File NOT found: {full_path}")

print("\n" + "=" * 80)
