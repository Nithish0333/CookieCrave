#!/usr/bin/env python
"""
Quick Change Gourmet Chocolates #8 Image
Automatically pick a different gourmet chocolate image
"""
import os
import sys
import requests
from io import BytesIO
from PIL import Image
import django

# Setup Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# Pixels API
PIXELS_API_KEY = "G6NINarEcSMRLL4hKyP8pq2aLfLJRuSxZGhPoQmEtoKZNtW7XftIaHpP"

def change_gourmet_image():
    """Change Gourmet Chocolates #8 to a different image"""
    print("🍫 Changing Gourmet Chocolates #8 Image")
    print("=" * 45)
    
    try:
        product = Product.objects.get(name='Gourmet Chocolates #8')
        print(f"✅ Found: {product.name}")
        
        # Show current image
        if product.image_url:
            current_url = product.image_url
            print(f"🌐 Current URL: {current_url}")
        
        # Get new gourmet chocolate images
        headers = {"Authorization": PIXELS_API_KEY}
        params = {"query": "gourmet chocolates", "per_page": 20, "orientation": "square"}
        
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            photos = data.get('photos', [])
            
            # Find a different image (not the current one)
            new_photo = None
            for photo in photos:
                photo_url = photo.get('src', {}).get('original') or photo.get('src', {}).get('large2x') or photo.get('src', {}).get('large')
                if photo_url != current_url:
                    new_photo = photo
                    break
            
            if new_photo:
                image_url = new_photo.get('src', {}).get('original') or new_photo.get('src', {}).get('large2x') or new_photo.get('src', {}).get('large')
                photographer = new_photo.get('photographer', 'Unknown')
                
                print(f"\n📥 New image from: {photographer}")
                print(f"   URL: {image_url[:60]}...")
                
                # Download and process
                response = requests.get(image_url, timeout=15)
                response.raise_for_status()
                
                img = Image.open(BytesIO(response.content))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=85, optimize=True)
                image_data = buffer.getvalue()
                
                # Update product
                product.image_data = image_data
                product.image_url = image_url
                product.save()
                
                print(f"✅ SUCCESS! Image updated")
                print(f"   📊 New size: {len(image_data)} bytes")
                print(f"   📸 By: {photographer}")
                print(f"   🔄 Refresh frontend to see change!")
                
            else:
                print(f"❌ No different images found")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Product.DoesNotExist:
        print(f"❌ Product not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    change_gourmet_image()
