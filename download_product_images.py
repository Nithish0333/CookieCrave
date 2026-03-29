#!/usr/bin/env python
"""
Download product images locally using Unsplash API.
Images will be saved to backend/media/product_images/
"""

import os
import sys
import django
import requests
from urllib.parse import urlparse
from pathlib import Path

# Setup Django
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# Unsplash download URLs (no authentication needed)
PRODUCT_IMAGES = {
    'Classic Chocolate Chip Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Double Chocolate Chip': 'https://images.unsplash.com/photo-1587080195348-c5ddb7dd5433?w=800&q=80',
    'White Chocolate Chip': 'https://images.unsplash.com/photo-1599599810694-b5ac4dd33826?w=800&q=80',
    'Chocolate Cake Slice': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Vanilla Cake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Strawberry Cake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Chocolate Milkshake': 'https://images.unsplash.com/photo-1586985289688-cacf60880ccf?w=800&q=80',
    'Vanilla Milkshake': 'https://images.unsplash.com/photo-1586985289688-cacf60880ccf?w=800&q=80',
    'Strawberry Milkshake': 'https://images.unsplash.com/photo-1553530889-e6cf89870560?w=800&q=80',
    'Dark Chocolate Bar': 'https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=800&q=80',
    'Milk Chocolate Bar': 'https://images.unsplash.com/photo-1599599810694-b5ac4dd33826?w=800&q=80',
    'Chocolate Truffles': 'https://images.unsplash.com/photo-1599599810694-b5ac4dd33826?w=800&q=80',
    'Almond Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Cranberry Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Walnut Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Oatmeal Raisin Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
    'Oatmeal Honey Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
    'Oatmeal Cranberry Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
}

def get_safe_filename(product_name):
    """Convert product name to safe filename"""
    return product_name.lower().replace(' ', '_').replace('/', '_') + '.jpg'

def download_images():
    """Download all product images"""
    print("=" * 80)
    print("DOWNLOADING PRODUCT IMAGES")
    print("=" * 80)
    
    # Create media directory if it doesn't exist
    media_dir = Path('media/product_images')
    media_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = 0
    failed = 0
    
    for product_name, image_url in PRODUCT_IMAGES.items():
        filename = get_safe_filename(product_name)
        filepath = media_dir / filename
        
        try:
            # Check if already downloaded
            if filepath.exists():
                print(f"✅ {product_name}")
                print(f"   └─ Already exists: {filename}")
                downloaded += 1
                continue
            
            # Download image
            print(f"⏳ Downloading: {product_name}...", end=" ")
            response = requests.get(image_url, timeout=10)
            
            if response.status_code == 200:
                # Save image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                file_size = filepath.stat().st_size / 1024  # KB
                print(f"✅ ({file_size:.1f}KB)")
                print(f"   └─ Saved: {filename}")
                downloaded += 1
            else:
                print(f"❌ (HTTP {response.status_code})")
                failed += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"✅ Downloaded: {downloaded}/{len(PRODUCT_IMAGES)}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Location: {media_dir.absolute()}")
    print("=" * 80)

if __name__ == '__main__':
    download_images()
