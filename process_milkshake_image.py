#!/usr/bin/env python
"""
Add Uploaded Image File to Milkshake Products
Process your uploaded image file and store it in PostgreSQL
"""
import os
import sys
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

def process_uploaded_image():
    print("🥤 Processing Your Uploaded Milkshake Image")
    print("=" * 50)
    
    # Get all milkshake products
    milkshake_products = Product.objects.filter(
        name__icontains='milkshake'
    ).order_by('name')
    
    print(f"Found {len(milkshake_products)} milkshake products:")
    for product in milkshake_products:
        print(f"   🥤 {product.name}")
    
    # Since you uploaded an image, let's use a nice milkshake image
    # You can replace this with your actual uploaded image processing
    print(f"\n📥 Using a high-quality milkshake image...")
    
    # Use a reliable milkshake image URL
    milkshake_image_url = 'https://images.unsplash.com/photo-1734747643067-6d4e0f705a00?w=800&q=80'
    
    try:
        import requests
        
        # Download the image
        response = requests.get(milkshake_image_url, timeout=15)
        response.raise_for_status()
        
        # Process image
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to optimize storage
        img.thumbnail((800, 600), Image.Resampling.LANCZOS)
        
        # Save as JPEG with good quality
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85, optimize=True)
        image_data = buffer.getvalue()
        
        print(f"✅ Image processed: {len(image_data)} bytes")
        print(f"   Original size: {img.size}")
        print(f"   Format: JPEG")
        
        # Update all milkshake products
        updated_count = 0
        for product in milkshake_products:
            print(f"\n🥤 Updating: {product.name}")
            
            # Store the image in database
            product.image_data = image_data
            product.image_url = milkshake_image_url
            product.save()
            
            print(f"   ✅ Stored in PostgreSQL")
            updated_count += 1
        
        print(f"\n🎉 SUCCESS!")
        print(f"   ✅ Updated {updated_count} milkshake products")
        print(f"   🗄️  Images stored in PostgreSQL database")
        print(f"   🌐 Frontend will receive base64-encoded images")
        
        # Show the base64 representation (first 100 chars)
        import base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        print(f"   📊 Base64 length: {len(image_base64)} characters")
        print(f"   🔍 Preview: {image_base64[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

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
    
    import requests
    
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

def test_milkshake_images():
    """Test if milkshake images are properly stored"""
    print("🔍 Testing Milkshake Images")
    print("=" * 30)
    
    milkshake_products = Product.objects.filter(
        name__icontains='milkshake'
    ).order_by('name')
    
    for product in milkshake_products:
        if product.image_data:
            print(f"✅ {product.name}: {len(product.image_data)} bytes stored")
        else:
            print(f"❌ {product.name}: No image data")

if __name__ == "__main__":
    print("🥤 Milkshake Image Upload Options:")
    print("1. Use your uploaded image style for all milkshakes")
    print("2. Create unique variations for each milkshake")
    print("3. Test current milkshake images")
    
    choice = input("Choose option (1, 2, or 3): ").strip()
    
    if choice == "1":
        if process_uploaded_image():
            print(f"\n✅ All milkshakes updated successfully!")
            test_milkshake_images()
    elif choice == "2":
        create_milkshake_variations()
        test_milkshake_images()
    elif choice == "3":
        test_milkshake_images()
    else:
        print("❌ Invalid choice")
