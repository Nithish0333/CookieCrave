#!/usr/bin/env python
"""
Add User's Image to Milkshake Products
Upload the provided image to all milkshake products
"""
import os
import sys
import requests
from io import BytesIO
from PIL import Image
import base64
import django

# Setup Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def add_image_to_milkshakes():
    print("🥤 Adding Your Image to Milkshake Products")
    print("=" * 50)
    
    # Get all milkshake products
    milkshake_products = Product.objects.filter(
        name__icontains='milkshake'
    ).order_by('name')
    
    print(f"Found {len(milkshake_products)} milkshake products:")
    for product in milkshake_products:
        print(f"   🥤 {product.name}")
    
    # Your uploaded image - replace with your actual image URL or file path
    # Option 1: If you have the image URL
    image_url = input("Enter your milkshake image URL (or press Enter to use default): ").strip()
    
    if not image_url:
        # Use a nice default milkshake image
        image_url = 'https://images.unsplash.com/photo-1734747643067-6d4e0f705a00?w=800&q=80'
        print(f"Using default milkshake image: {image_url}")
    
    try:
        # Download the image
        print(f"\n📥 Downloading image...")
        response = requests.get(image_url, timeout=15)
        response.raise_for_status()
        
        # Process image
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to optimize storage
        img.thumbnail((800, 600), Image.Resampling.LANCZOS)
        
        # Save as JPEG
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85, optimize=True)
        image_data = buffer.getvalue()
        
        print(f"✅ Image processed: {len(image_data)} bytes")
        
        # Update all milkshake products
        updated_count = 0
        for product in milkshake_products:
            print(f"\n🥤 Updating: {product.name}")
            
            # Store the same image for all milkshakes, or create variations
            product.image_data = image_data
            product.image_url = image_url
            product.save()
            
            print(f"   ✅ Stored in PostgreSQL")
            updated_count += 1
        
        print(f"\n🎉 SUCCESS!")
        print(f"   ✅ Updated {updated_count} milkshake products")
        print(f"   🗄️  Images stored in PostgreSQL database")
        print(f"   🌐 Frontend will receive base64-encoded images")
        
        # Test the result
        print(f"\n🔍 Testing one milkshake product...")
        test_product = milkshake_products.first()
        if test_product.image_data:
            print(f"   ✅ {test_product.name} has image data ({len(test_product.image_data)} bytes)")
        else:
            print(f"   ❌ No image data found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Please check your image URL and try again")

def create_milkshake_variations():
    """Create different variations for each milkshake product"""
    print("🎨 Creating Unique Variations for Each Milkshake")
    print("=" * 55)
    
    # Different milkshake image URLs for variety
    milkshake_urls = [
        'https://images.unsplash.com/photo-1734747643067-6d4e0f705a00?w=800&q=80',  # Chocolate
        'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',  # Vanilla
        'https://images.unsplash.com/photo-1553530889-e6cf89870560?w=800&q=80',  # Strawberry
        'https://images.unsplash.com/photo-1522249341405-3871994ac062?w=800&q=80',  # Dark chocolate
        'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=800&q=80',  # Mixed berry
        'https://images.unsplash.com/photo-1598968333180-9b4f6bc2bf52?w=800&q=80',  # Special
    ]
    
    milkshake_products = Product.objects.filter(
        name__icontains='milkshake'
    ).order_by('name')
    
    print(f"Updating {len(milkshake_products)} milkshakes with unique images...")
    
    for i, product in enumerate(milkshake_products):
        # Use different URL for each milkshake
        url = milkshake_urls[i % len(milkshake_urls)]
        
        try:
            print(f"\n🥤 {product.name} -> {url[-30:]}")
            
            # Download and process
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((800, 600), Image.Resampling.LANCZOS)
            
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85, optimize=True)
            image_data = buffer.getvalue()
            
            # Store in database
            product.image_data = image_data
            product.image_url = url
            product.save()
            
            print(f"   ✅ Stored ({len(image_data)} bytes)")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🥤 Milkshake Image Upload Options:")
    print("1. Use your uploaded image for all milkshakes")
    print("2. Create unique variations for each milkshake")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        add_image_to_milkshakes()
    elif choice == "2":
        create_milkshake_variations()
    else:
        print("❌ Invalid choice")
