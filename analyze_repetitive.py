#!/usr/bin/env python
"""
Analyze Repetitive Images
Check why you're still seeing repetitive images
"""
import requests
from collections import Counter

def analyze_repetitive_images():
    print("🔍 Analyzing Repetitive Images")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:8000/api/products/', timeout=10)
        data = response.json()
        
        print(f"✅ API Response Status: {response.status_code}")
        print(f"📦 Total Products: {len(data)}")
        
        # Count image URLs
        url_counts = Counter()
        base64_counts = Counter()
        
        postgresql_images = []
        url_images = []
        
        for product in data:
            image = product.get('image', 'NO IMAGE')
            name = product.get('name', 'Unknown')
            
            if image.startswith('data:image/jpeg;base64,'):
                # PostgreSQL images
                postgresql_images.append((name, image))
                base64_counts[image] += 1
            elif image.startswith('https://'):
                # URL images
                url_images.append((name, image))
                url_counts[image] += 1
            else:
                print(f"⚠️  {name}: {image[:50]}...")
        
        print(f"\n📊 Image Distribution:")
        print(f"   🗄️  PostgreSQL images: {len(postgresql_images)}")
        print(f"   🌐 URL images: {len(url_images)}")
        
        # Check for repetitive URLs
        if url_counts:
            print(f"\n🔄 URL Image Repetition Analysis:")
            most_common = url_counts.most_common(10)
            
            for url, count in most_common:
                if count > 1:
                    print(f"   ❌ REPEATED {count} times: {url[-50:]}")
                    
                    # Show which products use this URL
                    products_with_url = [name for name, img in url_images if img == url]
                    print(f"      Products: {', '.join(products_with_url[:3])}")
                    if len(products_with_url) > 3:
                        print(f"      ... and {len(products_with_url) - 3} more")
                else:
                    print(f"   ✅ Used once: {url[-50:]}")
        
        # Check base64 repetition
        if base64_counts:
            print(f"\n🔄 PostgreSQL Image Repetition:")
            for base64, count in base64_counts.items():
                if count > 1:
                    print(f"   ⚠️  Same image used {count} times")
                else:
                    print(f"   ✅ Unique image")
        
        # Show the problem
        print(f"\n🎯 PROBLEM IDENTIFIED:")
        print(f"   You have {len(url_images)} products still using external URLs")
        print(f"   These URLs might be repetitive or broken")
        print(f"   Only {len(postgresql_images)} products have PostgreSQL images")
        
        print(f"\n🔧 SOLUTION:")
        print(f"   1. Convert all URL images to PostgreSQL images")
        print(f"   2. Use unique images for each product")
        print(f"   3. Run: python interactive_image_upload.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    analyze_repetitive_images()
