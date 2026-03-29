import os
import django
import requests
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def update_with_verified_unsplash():
    """Update products with verified working Unsplash URLs"""
    
    # Verified working Unsplash URLs for CookieCrave products
    verified_urls = {
        'Classic Chocolate Chip Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
        'Double Chocolate Chip': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&h=600&fit=crop',
        'White Chocolate Chip': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
        'Chocolate Cake Slice': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&h=600&fit=crop',
        'Vanilla Cake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&h=600&fit=crop',
        'Strawberry Cake': 'https://images.unsplash.com/photo-1464975911061-772ca6b0ce0d?w=800&h=600&fit=crop',
        'Chocolate Milkshake': 'https://images.unsplash.com/photo-1555939594-58d7cb561a1a?w=800&h=600&fit=crop',
        'Vanilla Milkshake': 'https://images.unsplash.com/photo-1555939594-58d7cb561a1a?w=800&h=600&fit=crop',
        'Strawberry Milkshake': 'https://images.unsplash.com/photo-1555939594-58d7cb561a1a?w=800&h=600&fit=crop',
        'Dark Chocolate Bar': 'https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=800&h=600&fit=crop',
        'Milk Chocolate Bar': 'https://images.unsplash.com/photo-1599599810694-b5ac4dd33826?w=800&h=600&fit=crop',
        'Chocolate Truffles': 'https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=800&h=600&fit=crop',
        'Almond Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
        'Cranberry Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
        'Walnut Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
        'Oatmeal Raisin Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
        'Oatmeal Honey Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
        'Oatmeal Cranberry Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
    }
    
    print("🎨 Updating CookieCrave products with verified Unsplash images...")
    print("=" * 60)
    
    updated_count = 0
    failed_count = 0
    
    for product in Product.objects.all():
        product_name = product.name
        
        # Get verified URL
        unsplash_url = verified_urls.get(product_name)
        
        if unsplash_url:
            try:
                # Test if the image is accessible (with shorter timeout)
                response = requests.get(unsplash_url, timeout=5)
                
                if response.status_code == 200:
                    # Update product image
                    product.image = unsplash_url
                    product.save()
                    updated_count += 1
                    print(f"✅ Updated {product_name}")
                    print(f"   📸 {unsplash_url}")
                else:
                    print(f"❌ Image not accessible for {product_name}: {response.status_code}")
                    failed_count += 1
                    
            except Exception as e:
                print(f"❌ Error updating {product_name}: {str(e)}")
                failed_count += 1
        else:
            print(f"⚠️ No Unsplash image mapped for {product_name}")
            failed_count += 1
    
    print(f"\n📊 Summary:")
    print(f"✅ Successfully updated: {updated_count} products")
    print(f"❌ Failed: {failed_count} products")
    print(f"📈 Success rate: {updated_count/(updated_count+failed_count)*100:.1f}%")
    
    return updated_count

def test_current_images():
    """Test current product images"""
    print("📸 Testing current product images...")
    print("=" * 40)
    
    products = Product.objects.all()[:5]  # Test first 5
    
    for product in products:
        image_url = str(product.image) if product.image else 'None'
        print(f"\n🍪 {product.name}:")
        print(f"   URL: {image_url}")
        
        if image_url and image_url.startswith('http'):
            try:
                response = requests.get(image_url, timeout=3)
                if response.status_code == 200:
                    size_kb = len(response.content) / 1024
                    print(f"   ✅ Working ({size_kb:.1f} KB)")
                else:
                    print(f"   ❌ Error: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:30]}")
        else:
            print(f"   ⚠️ Not a valid URL")

if __name__ == "__main__":
    print("🎨 CookieCrave Unsplash Image Updater")
    print("=" * 40)
    
    # Test current images first
    test_current_images()
    
    print("\n🚀 Starting Unsplash image update...")
    update_with_verified_unsplash()
