#!/usr/bin/env python
import requests
import json

print("=" * 80)
print("CHECKING FRONTEND API RESPONSE")
print("=" * 80)

try:
    # Test API as frontend would
    response = requests.get('http://localhost:8000/api/products/')
    data = response.json()
    
    print(f"\n✅ API Response Status: {response.status_code}")
    print(f"📦 Total Products: {len(data)}")
    
    print("\n📋 First 3 Products:")
    for i, product in enumerate(data[:3], 1):
        print(f"\n{i}. {product.get('name')}")
        print(f"   - ID: {product.get('id')}")
        print(f"   - Price: ${product.get('price')}")
        print(f"   - Image: {product.get('image')}")
        print(f"   - Category: {product.get('category_name')}")
        
        # Check if image field exists
        if 'image' in product:
            print(f"   ✅ 'image' field present")
        else:
            print(f"   ❌ 'image' field MISSING")
        
        print(f"   - Keys in response: {list(product.keys())}")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
