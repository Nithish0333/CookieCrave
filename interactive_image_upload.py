#!/usr/bin/env python
"""
Interactive Image Upload Tool
Step-by-step guide to upload your selected images
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

def test_image_url(url):
    """Test if an image URL is accessible"""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def download_and_store_image(product_name, image_url):
    """Download and store image for a specific product"""
    try:
        print(f"   📥 Downloading: {product_name}")
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
        
        # Find and update the product
        product = Product.objects.get(name=product_name)
        product.image_data = image_data
        product.image_url = image_url
        product.save()
        
        print(f"   ✅ Stored: {len(image_data)} bytes")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def interactive_upload():
    """Interactive tool to upload images one by one"""
    print("🖼️  INTERACTIVE IMAGE UPLOAD TOOL")
    print("=" * 50)
    
    # Show all products that need images
    products_needing_images = Product.objects.filter(image_data__isnull=True).order_by('name')
    
    print(f"\n📋 Products needing images: {len(products_needing_images)}")
    for i, product in enumerate(products_needing_images[:10], 1):
        print(f"   {i:2}. {product.name}")
    
    if len(products_needing_images) > 10:
        print(f"   ... and {len(products_needing_images) - 10} more")
    
    print(f"\n🔧 Instructions:")
    print(f"1. Choose a product from the list")
    print(f"2. Find a suitable image URL")
    print(f"3. Enter the product number and URL")
    print(f"4. I'll download and store it for you")
    
    while True:
        print(f"\n" + "="*50)
        try:
            choice = input(f"Enter product number (1-{len(products_needing_images)}) or 'quit': ").strip()
            
            if choice.lower() == 'quit':
                break
            
            choice_num = int(choice)
            if choice_num < 1 or choice_num > len(products_needing_images):
                print(f"❌ Invalid number. Choose 1-{len(products_needing_images)}")
                continue
            
            product = products_needing_images[choice_num - 1]
            print(f"\n🍪 Selected: {product.name}")
            
            url = input(f"Enter image URL for '{product.name}': ").strip()
            
            if not url:
                print(f"❌ No URL provided")
                continue
            
            # Test the URL first
            if not test_image_url(url):
                print(f"❌ URL is not accessible. Please check and try again.")
                continue
            
            # Download and store
            if download_and_store_image(product.name, url):
                print(f"✅ Success! Image stored for {product.name}")
                # Refresh the list
                products_needing_images = Product.objects.filter(image_data__isnull=True).order_by('name')
                if not products_needing_images:
                    print(f"\n🎉 All products now have images!")
                    break
            else:
                print(f"❌ Failed to store image. Please try another URL.")
                
        except ValueError:
            print(f"❌ Please enter a valid number")
        except KeyboardInterrupt:
            print(f"\n👋 Goodbye!")
            break
    
    # Show final status
    total_products = Product.objects.count()
    products_with_images = Product.objects.filter(image_data__isnull=False).count()
    
    print(f"\n📊 Final Status:")
    print(f"   Total products: {total_products}")
    print(f"   With images: {products_with_images}")
    print(f"   Still needed: {total_products - products_with_images}")

def batch_upload():
    """Batch upload using predefined URLs"""
    print("📦 BATCH IMAGE UPLOAD")
    print("=" * 30)
    
    # Your predefined image URLs go here
    PRODUCT_IMAGES = {
        # Add your 48 image URLs here
        # Example:
        # 'Classic Chocolate Chip Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    }
    
    if not PRODUCT_IMAGES:
        print("❌ No images defined. Please add URLs to PRODUCT_IMAGES dictionary")
        return
    
    success = 0
    failed = 0
    
    for product_name, image_url in PRODUCT_IMAGES.items():
        if download_and_store_image(product_name, image_url):
            success += 1
        else:
            failed += 1
    
    print(f"\n📊 Batch Upload Results:")
    print(f"   ✅ Success: {success}")
    print(f"   ❌ Failed: {failed}")

if __name__ == "__main__":
    print("Choose upload method:")
    print("1. Interactive (one by one)")
    print("2. Batch upload (predefined URLs)")
    
    method = input("Enter choice (1 or 2): ").strip()
    
    if method == "1":
        interactive_upload()
    elif method == "2":
        batch_upload()
    else:
        print("❌ Invalid choice")
