#!/usr/bin/env python
"""
PostgreSQL Image Management System
Download and store images directly in PostgreSQL database
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

def download_and_store_image(product_name, image_url, max_size=(800, 600)):
    """Download image from URL, resize it, and store as binary data"""
    try:
        # Download image
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Open and resize image
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image to reduce storage size
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save to bytes buffer
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85, optimize=True)
        image_data = buffer.getvalue()
        
        return image_data
        
    except Exception as e:
        print(f"❌ Error processing {product_name}: {e}")
        return None

def update_product_images():
    """Update all products with downloaded images stored in PostgreSQL"""
    print("🖼️  PostgreSQL Image Storage System")
    print("=" * 50)
    
    # Define your manually selected images for each product
    # You should replace these with your actual downloaded images
    PRODUCT_IMAGES = {
        'Classic Chocolate Chip Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
        'Double Chocolate Chip': 'https://images.unsplash.com/photo-1556969092-0b42e2ca37ea?w=800&q=80',
        'White Chocolate Chip': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
        'Almond Cookies': 'https://images.unsplash.com/photo-1598968333180-9b4f6bc2bf52?w=800&q=80',
        'Cranberry Cookies': 'https://images.unsplash.com/photo-1604466513550-3272a4927541?w=800&q=80',
        'Walnut Cookies': 'https://images.unsplash.com/photo-1514529470165-75021c6cc623?w=800&q=80',
        'Oatmeal Raisin Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
        'Oatmeal Honey Cookies': 'https://images.unsplash.com/photo-1586191372612-6b5a50788e76?w=800&q=80',
        'Oatmeal Cranberry Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
        'Chocolate Cake Slice': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
        'Vanilla Cake': 'https://images.unsplash.com/photo-1464349095981-7f2c70667386?w=800&q=80',
        'Strawberry Cake': 'https://images.unsplash.com/photo-1563729784474-dfbb5446cced?w=800&q=80',
        'Chocolate Milkshake': 'https://images.unsplash.com/photo-1734747643067-6d4e0f705a00?w=800&q=80',
        'Vanilla Milkshake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
        'Strawberry Milkshake': 'https://images.unsplash.com/photo-1553530889-e6cf89870560?w=800&q=80',
        'Dark Chocolate Bar': 'https://images.unsplash.com/photo-1522249341405-3871994ac062?w=800&q=80',
        'Milk Chocolate Bar': 'https://images.unsplash.com/photo-1546069201-fa0afd4b5d0a?w=800&q=80',
        'Chocolate Truffles': 'https://images.unsplash.com/photo-1596792503312-7e85e0b8c7a2?w=800&q=80',
        # Add more products as needed...
    }
    
    updated_count = 0
    error_count = 0
    
    products = Product.objects.all()
    print(f"Found {len(products)} products")
    
    for product in products:
        print(f"\n🍪 Processing: {product.name}")
        
        # Get image URL from your predefined list or use a default
        image_url = PRODUCT_IMAGES.get(product.name, 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80')
        
        # Download and store image
        image_data = download_and_store_image(product.name, image_url)
        
        if image_data:
            # Store in database
            product.image_data = image_data
            product.image_url = image_url  # Keep reference to original URL
            product.save()
            
            print(f"   ✅ Stored image ({len(image_data)} bytes)")
            updated_count += 1
        else:
            print(f"   ❌ Failed to process image")
            error_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Updated: {updated_count} products")
    print(f"   ❌ Errors: {error_count} products")
    print(f"   🗄️  Images stored in PostgreSQL database")

if __name__ == "__main__":
    update_product_images()
