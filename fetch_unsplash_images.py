import os
import django
import requests
import json
from urllib.parse import quote
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, Category

def get_unsplash_images():
    """Fetch food images from Unsplash API for CookieCrave products"""
    
    # Get API key from environment (you'll need to add this)
    access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    if not access_key or access_key == 'your-unsplash-access-key-here':
        print("❌ Please set your Unsplash Access Key in .env file")
        print("📝 Steps:")
        print("1. Go to: https://unsplash.com/developers")
        print("2. Create a new application")
        print("3. Get your Access Key")
        print("4. Add to .env: UNSPLASH_ACCESS_KEY=your-key-here")
        print("\n🔍 Using demo mode with curated Unsplash URLs...")
        return use_demo_unsplash_images()
    
    # Product search terms mapping for Unsplash
    product_search_terms = {
        'Classic Chocolate Chip Cookies': 'chocolate chip cookies',
        'Double Chocolate Chip': 'double chocolate cookies',
        'White Chocolate Chip': 'white chocolate cookies',
        'Chocolate Cake Slice': 'chocolate cake slice',
        'Vanilla Cake': 'vanilla cake',
        'Strawberry Cake': 'strawberry cake',
        'Chocolate Milkshake': 'chocolate milkshake',
        'Vanilla Milkshake': 'vanilla milkshake',
        'Strawberry Milkshake': 'strawberry milkshake',
        'Dark Chocolate Bar': 'dark chocolate bar',
        'Milk Chocolate Bar': 'milk chocolate bar',
        'Chocolate Truffles': 'chocolate truffles',
        'Almond Cookies': 'almond cookies',
        'Cranberry Cookies': 'cranberry cookies',
        'Walnut Cookies': 'walnut cookies',
        'Oatmeal Raisin Cookies': 'oatmeal raisin cookies',
        'Oatmeal Honey Cookies': 'oatmeal honey cookies',
        'Oatmeal Cranberry Cookies': 'oatmeal cranberry cookies',
    }
    
    print("📸 Fetching food images from Unsplash API...")
    print(f"🔑 Using Access Key: {access_key[:10]}...{access_key[-4:]}")
    
    updated_count = 0
    failed_count = 0
    
    for product in Product.objects.all():
        product_name = product.name
        
        # Get search term for this product
        search_term = product_search_terms.get(product_name, product_name.lower())
        
        try:
            # Search for photos on Unsplash
            search_url = "https://api.unsplash.com/search/photos"
            headers = {
                'Authorization': f'Client-ID {access_key}'
            }
            params = {
                'query': search_term,
                'per_page': 10,  # Get 10 results
                'orientation': 'landscape',  # Get landscape images
                'content_filter': 'high',  # High quality images only
            }
            
            print(f"🔍 Searching for: {search_term}")
            response = requests.get(search_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('results') and len(data['results']) > 0:
                    # Get the first high-quality result
                    photo = data['results'][0]
                    image_url = photo['urls']['regular']  # Regular size (1080x720)
                    
                    # Also store attribution info
                    photographer = photo['user']['name']
                    photo_url = photo['links']['html']
                    
                    # Update product image
                    product.image = image_url
                    product.save()
                    updated_count += 1
                    print(f"✅ Updated {product_name}")
                    print(f"   📸 {image_url}")
                    print(f"   📷 Photo by: {photographer}")
                else:
                    print(f"⚠️ No results found for {product_name}")
                    failed_count += 1
            else:
                print(f"❌ API error for {product_name}: {response.status_code}")
                if response.status_code == 401:
                    print("   Check your Unsplash Access Key")
                elif response.status_code == 403:
                    print("   Rate limit exceeded. Waiting...")
                    import time
                    time.sleep(2)
                failed_count += 1
                
        except Exception as e:
            print(f"❌ Error fetching image for {product_name}: {str(e)}")
            failed_count += 1
        
        # Small delay to avoid rate limiting
        import time
        time.sleep(1)
    
    print(f"\n📊 Summary:")
    print(f"✅ Successfully updated: {updated_count} products")
    print(f"❌ Failed: {failed_count} products")
    print(f"📈 Success rate: {updated_count/(updated_count+failed_count)*100:.1f}%")

def use_demo_unsplash_images():
    """Use curated high-quality Unsplash URLs without API key"""
    
    # Curated Unsplash image URLs for CookieCrave products
    unsplash_images = {
        'Classic Chocolate Chip Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1080&h=720&fit=crop',
        'Double Chocolate Chip': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=1080&h=720&fit=crop',
        'White Chocolate Chip': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1080&h=720&fit=crop',
        'Chocolate Cake Slice': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=1080&h=720&fit=crop',
        'Vanilla Cake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=1080&h=720&fit=crop',
        'Strawberry Cake': 'https://images.unsplash.com/photo-1464975911061-772ca6b0ce0d?w=1080&h=720&fit=crop',
        'Chocolate Milkshake': 'https://images.unsplash.com/photo-1555939594-58d7cb561a1a?w=1080&h=720&fit=crop',
        'Vanilla Milkshake': 'https://images.unsplash.com/photo-1555939594-58d7cb561a1a?w=1080&h=720&fit=crop',
        'Strawberry Milkshake': 'https://images.unsplash.com/photo-1555939594-58d7cb561a1a?w=1080&h=720&fit=crop',
        'Dark Chocolate Bar': 'https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=1080&h=720&fit=crop',
        'Milk Chocolate Bar': 'https://images.unsplash.com/photo-1599599810694-b5ac4dd33826?w=1080&h=720&fit=crop',
        'Chocolate Truffles': 'https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=1080&h=720&fit=crop',
        'Almond Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1080&h=720&fit=crop',
        'Cranberry Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1080&h=720&fit=crop',
        'Walnut Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1080&h=720&fit=crop',
        'Oatmeal Raisin Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1080&h=720&fit=crop',
        'Oatmeal Honey Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1080&h=720&fit=crop',
        'Oatmeal Cranberry Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1080&h=720&fit=crop',
    }
    
    print("🎨 Using curated Unsplash images for CookieCrave products...")
    print("=" * 50)
    
    updated_count = 0
    
    for product in Product.objects.all():
        product_name = product.name
        
        # Get Unsplash image URL
        unsplash_url = unsplash_images.get(product_name)
        
        if unsplash_url:
            try:
                # Test if the image is accessible
                response = requests.get(unsplash_url, timeout=10)
                
                if response.status_code == 200:
                    # Update product image
                    product.image = unsplash_url
                    product.save()
                    updated_count += 1
                    print(f"✅ Updated {product_name}")
                    print(f"   📸 {unsplash_url}")
                else:
                    print(f"❌ Image not accessible for {product_name}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error updating {product_name}: {str(e)}")
        else:
            print(f"⚠️ No Unsplash image mapped for {product_name}")
    
    print(f"\n📊 Summary:")
    print(f"✅ Successfully updated: {updated_count} products")
    print(f"📸 Using high-quality Unsplash images")
    
    return updated_count

def test_unsplash_images():
    """Test a few Unsplash image URLs"""
    
    test_urls = [
        'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=1080&h=720&fit=crop',
        'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=1080&h=720&fit=crop',
        'https://images.unsplash.com/photo-1555939594-58d7cb561a1a?w=1080&h=720&fit=crop',
        'https://images.unsplash.com/photo-1559056199-641a0ac8b3f4?w=1080&h=720&fit=crop'
    ]
    
    print("🎨 Testing Unsplash image URLs:")
    print("=" * 40)
    
    for i, url in enumerate(test_urls, 1):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                size_kb = len(response.content) / 1024
                print(f"{i}. ✅ Working ({size_kb:.1f} KB)")
                print(f"   {url}")
            else:
                print(f"{i}. ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"{i}. ❌ Error: {str(e)[:30]}")
        print()

if __name__ == "__main__":
    print("🎨 CookieCrave Unsplash Image Fetcher")
    print("=" * 40)
    
    # Test Unsplash images first
    print("🔍 Testing Unsplash image accessibility...")
    test_unsplash_images()
    
    print("\n🚀 Starting image replacement...")
    get_unsplash_images()
