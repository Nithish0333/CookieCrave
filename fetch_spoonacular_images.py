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

def get_spoonacular_images():
    """Fetch food images from Spoonacular API for CookieCrave products"""
    
    # Get API key from environment
    api_key = os.getenv('SPOONACULAR_API_KEY')
    if not api_key or api_key == 'your-spoonacular-api-key-here':
        print("❌ Please set your Spoonacular API key in .env file")
        print("Get your free API key from: https://spoonacular.com/food-api")
        return
    
    # Product search terms mapping
    product_search_terms = {
        'Classic Chocolate Chip Cookies': 'chocolate chip cookies',
        'Double Chocolate Chip': 'double chocolate chip cookies',
        'White Chocolate Chip': 'white chocolate chip cookies',
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
    
    print("🍪 Fetching food images from Spoonacular API...")
    print(f"📸 Using API key: {api_key[:10]}...{api_key[-4:]}")
    
    updated_count = 0
    failed_count = 0
    
    for product in Product.objects.all():
        product_name = product.name
        
        # Get search term for this product
        search_term = product_search_terms.get(product_name, product_name.lower())
        
        try:
            # Search for food images
            search_url = f"https://api.spoonacular.com/food/ingredients/search"
            params = {
                'query': search_term,
                'number': 5,  # Get 5 results
                'apiKey': api_key
            }
            
            print(f"🔍 Searching for: {search_term}")
            response = requests.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('results') and len(data['results']) > 0:
                    # Get the first result's image
                    ingredient = data['results'][0]
                    image_url = ingredient.get('image')
                    
                    if image_url:
                        # Use the high-quality image URL
                        if image_url.startswith('https://spoonacular.com/cdn/ingredients_100x100/'):
                            # Replace with larger size
                            image_url = image_url.replace('ingredients_100x100', 'ingredients_500x500')
                        
                        # Update product image
                        product.image = image_url
                        product.save()
                        updated_count += 1
                        print(f"✅ Updated {product_name}: {image_url}")
                    else:
                        print(f"⚠️ No image found for {product_name}")
                        failed_count += 1
                else:
                    print(f"⚠️ No results found for {product_name}")
                    failed_count += 1
            else:
                print(f"❌ API error for {product_name}: {response.status_code}")
                if response.status_code == 401:
                    print("   Check your Spoonacular API key")
                elif response.status_code == 429:
                    print("   Rate limit exceeded. Waiting...")
                    import time
                    time.sleep(2)
                failed_count += 1
                
        except Exception as e:
            print(f"❌ Error fetching image for {product_name}: {str(e)}")
            failed_count += 1
        
        # Small delay to avoid rate limiting
        import time
        time.sleep(0.5)
    
    print(f"\n📊 Summary:")
    print(f"✅ Successfully updated: {updated_count} products")
    print(f"❌ Failed: {failed_count} products")
    print(f"📈 Success rate: {updated_count/(updated_count+failed_count)*100:.1f}%")

def test_api_connection():
    """Test Spoonacular API connection"""
    api_key = os.getenv('SPOONACULAR_API_KEY')
    if not api_key or api_key == 'your-spoonacular-api-key-here':
        print("❌ Please set your Spoonacular API key in .env file")
        return False
    
    try:
        # Test with a simple search
        url = "https://api.spoonacular.com/food/ingredients/search"
        params = {
            'query': 'chocolate chip cookies',
            'number': 1,
            'apiKey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                print("✅ Spoonacular API connection successful!")
                print(f"📸 Sample result: {data['results'][0]['name']}")
                return True
            else:
                print("⚠️ API connected but no results found")
                return False
        else:
            print(f"❌ API connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")
        return False

def show_sample_images():
    """Show sample images for a few products"""
    api_key = os.getenv('SPOONACULAR_API_KEY')
    if not api_key or api_key == 'your-spoonacular-api-key-here':
        print("❌ Please set your Spoonacular API key in .env file")
        return
    
    sample_products = ['chocolate chip cookies', 'chocolate cake', 'vanilla milkshake']
    
    print("🍪 Sample images from Spoonacular API:")
    print("=" * 50)
    
    for search_term in sample_products:
        try:
            url = "https://api.spoonacular.com/food/ingredients/search"
            params = {
                'query': search_term,
                'number': 3,
                'apiKey': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                print(f"\n🔍 {search_term.title()}:")
                for i, result in enumerate(results, 1):
                    name = result.get('name', 'Unknown')
                    image = result.get('image', '')
                    print(f"  {i}. {name}")
                    print(f"     📸 {image}")
            else:
                print(f"❌ Error fetching {search_term}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error with {search_term}: {str(e)}")

if __name__ == "__main__":
    print("🍪 CookieCrave Spoonacular Image Fetcher")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv('SPOONACULAR_API_KEY')
    if not api_key or api_key == 'your-spoonacular-api-key-here':
        print("❌ Please set your Spoonacular API key in .env file")
        print("📝 Steps:")
        print("1. Go to: https://spoonacular.com/food-api")
        print("2. Sign up for free account")
        print("3. Get your API key")
        print("4. Add to .env: SPOONACULAR_API_KEY=your-key-here")
        print("\n🔍 Running sample search to show available images...")
        show_sample_images()
    else:
        print("✅ API key found!")
        print("\n🔍 Testing API connection...")
        if test_api_connection():
            print("\n🚀 Starting image fetch...")
            get_spoonacular_images()
        else:
            print("\n❌ Please check your API key and connection")
