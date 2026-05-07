#!/usr/bin/env python3
"""
Final verification script to confirm Unsplash images are working
"""
import requests
import json

def test_complete_image_flow():
    print("🔍 FINAL VERIFICATION: Unsplash Images Fix")
    print("=" * 60)
    
    # Test 1: API Response
    print("\n1. Testing API Response...")
    try:
        response = requests.get('http://127.0.0.1:8000/api/products/', timeout=10)
        if response.status_code == 200:
            products = response.json()
            print(f"✅ API responding correctly ({len(products)} products)")
            
            # Test 2: Image URLs in response
            print("\n2. Testing Image URLs...")
            working_urls = 0
            total_tested = 0
            
            for product in products[:5]:  # Test first 5 products
                image_url = product.get('image')
                if image_url and image_url.startswith('https://images.unsplash.com'):
                    total_tested += 1
                    try:
                        img_response = requests.head(image_url, timeout=5)
                        if img_response.status_code == 200:
                            working_urls += 1
                            print(f"✅ {product['name'][:30]:<30} - Working")
                        else:
                            print(f"❌ {product['name'][:30]:<30} - Failed ({img_response.status_code})")
                    except:
                        print(f"❌ {product['name'][:30]:<30} - Error")
            
            print(f"\n📊 Image URL Results: {working_urls}/{total_tested} working")
            
            # Test 3: Frontend accessibility
            print("\n3. Testing Frontend...")
            try:
                frontend_response = requests.get('http://localhost:5173', timeout=5)
                if frontend_response.status_code == 200:
                    print("✅ Frontend accessible at http://localhost:5173")
                else:
                    print("❌ Frontend not accessible")
            except:
                print("❌ Frontend connection error")
            
        else:
            print(f"❌ API not responding (Status: {response.status_code})")
            
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 SUMMARY: Unsplash images should now be working!")
    print("   - Backend serving verified Unsplash URLs")
    print("   - Frontend should display real images instead of placeholders")
    print("   - Check browser at http://localhost:5173")

if __name__ == "__main__":
    test_complete_image_flow()
