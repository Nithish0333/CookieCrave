#!/usr/bin/env python
"""
Change Image for Gourmet Chocolates #8
Replace the current image with a new Pixels API image
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

def get_gourmet_chocolate_images():
    """Get new gourmet chocolate images from Pixels API"""
    print("🔍 Finding New Gourmet Chocolate Images")
    print("=" * 45)
    
    try:
        headers = {"Authorization": PIXELS_API_KEY}
        params = {"query": "gourmet chocolates", "per_page": 10, "orientation": "square"}
        
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            photos = data.get('photos', [])
            
            print(f"✅ Found {len(photos)} gourmet chocolate images:")
            
            for i, photo in enumerate(photos[:5], 1):
                photographer = photo.get('photographer', 'Unknown')
                image_url = photo.get('src', {}).get('original') or photo.get('src', {}).get('large2x') or photo.get('src', {}).get('large')
                print(f"   {i}. {photographer}")
                print(f"      {image_url[:60]}...")
            
            return photos
        else:
            print(f"❌ API Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def update_gourmet_chocolates_image():
    """Update Gourmet Chocolates #8 with a new image"""
    print("🍫 Updating Gourmet Chocolates #8")
    print("=" * 40)
    
    # Get the product
    try:
        product = Product.objects.get(name='Gourmet Chocolates #8')
        print(f"✅ Found product: {product.name}")
        
        # Show current image info
        if product.image_data:
            current_size = len(product.image_data)
            print(f"📊 Current image size: {current_size} bytes")
        if product.image_url:
            print(f"🌐 Current URL: {product.image_url}")
        
    except Product.DoesNotExist:
        print(f"❌ Product 'Gourmet Chocolates #8' not found")
        return
    
    # Get new images from Pixels API
    photos = get_gourmet_chocolate_images()
    
    if not photos:
        print("❌ No new images found")
        return
    
    # Let user choose or use the first one
    print(f"\n🎯 Choose a new image:")
    print(f"1. Use first image (recommended)")
    print(f"2. See more options")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        for i, photo in enumerate(photos[:10], 1):
            photographer = photo.get('photographer', 'Unknown')
            print(f"   {i}. {photographer}")
        
        try:
            photo_choice = int(input("Choose image number (1-10): ").strip())
            if 1 <= photo_choice <= len(photos):
                selected_photo = photos[photo_choice - 1]
            else:
                selected_photo = photos[0]
        except:
            selected_photo = photos[0]
    else:
        selected_photo = photos[0]
    
    # Get the image URL
    image_url = selected_photo.get('src', {}).get('original') or selected_photo.get('src', {}).get('large2x') or selected_photo.get('src', {}).get('large')
    photographer = selected_photo.get('photographer', 'Unknown')
    
    print(f"\n📥 Downloading new image from {photographer}")
    print(f"   URL: {image_url[:60]}...")
    
    try:
        # Download the image
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
        
        print(f"✅ Processed new image: {len(image_data)} bytes")
        print(f"   Original size: {img.size}")
        
        # Update the product
        product.image_data = image_data
        product.image_url = image_url
        product.save()
        
        print(f"✅ SUCCESS! Updated Gourmet Chocolates #8")
        print(f"   📊 New image size: {len(image_data)} bytes")
        print(f"   🌐 New URL stored: {image_url[:60]}...")
        print(f"   📸 Photographer: {photographer}")
        
        # Test the serializer
        from products.serializers import ProductSerializer
        serializer = ProductSerializer(product)
        serialized_image = serializer.data.get('image', '')
        
        if serialized_image.startswith('data:image'):
            print(f"✅ Serializer working correctly")
            print(f"   📊 Base64 length: {len(serialized_image)} chars")
        
        print(f"\n🎉 Image updated successfully!")
        print(f"🔄 Refresh your frontend to see the new image!")
        
    except Exception as e:
        print(f"❌ Error updating image: {e}")

def show_current_gourmet_image():
    """Show current Gourmet Chocolates #8 image info"""
    print("🔍 Current Gourmet Chocolates #8 Image")
    print("=" * 45)
    
    try:
        product = Product.objects.get(name='Gourmet Chocolates #8')
        
        print(f"Product: {product.name}")
        print(f"Category: {product.category.name if product.category else 'None'}")
        
        if product.image_data:
            size = len(product.image_data)
            print(f"✅ Has image_data: {size} bytes")
        else:
            print(f"❌ No image_data")
        
        if product.image_url:
            print(f"🌐 image_url: {product.image_url}")
        else:
            print(f"❌ No image_url")
            
    except Product.DoesNotExist:
        print(f"❌ Product 'Gourmet Chocolates #8' not found")

if __name__ == "__main__":
    print("🍫 GOURMET CHOCOLATES IMAGE UPDATER")
    print("Change image for Gourmet Chocolates #8")
    print("")
    print("Choose an option:")
    print("1. Show current image info")
    print("2. Update with new image")
    print("3. Both")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        show_current_gourmet_image()
    elif choice == "2":
        update_gourmet_chocolates_image()
    elif choice == "3":
        show_current_gourmet_image()
        update_gourmet_chocolates_image()
    else:
        print("❌ Invalid choice")
