import os
import django
import requests
import random
import time
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, Category
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_products_for_categories(target_count=10):
    access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    if not access_key or access_key == 'your-unsplash-access-key-here':
        print("❌ Please set your Unsplash Access Key in .env file")
        return
        
    print(f"📸 Generating up to {target_count} products per category from Unsplash...")
    
    # Get the site's default seller/admin to assign products to
    seller = User.objects.filter(is_staff=True).first()
    if not seller:
        seller = User.objects.first()
        if not seller:
            print("❌ No users found in database to assign as seller.")
            return

    adjectives = ["Deluxe", "Gourmet", "Signature", "Classic", "Premium", "Artisan", "Handcrafted", "Rich", "Ultimate", "Decadent"]

    for category in Category.objects.all():
        current_count = category.products.count()
        needed = target_count - current_count
        
        if needed <= 0:
            print(f"✅ {category.name} already has {current_count} products.")
            continue
            
        print(f"\n🔍 Need {needed} more products for category: {category.name}")
        
        try:
            search_url = "https://api.unsplash.com/search/photos"
            headers = {
                'Authorization': f'Client-ID {access_key}'
            }
            # Search term for Unsplash
            search_term = f"{category.name.lower()} dessert"
            
            # Fetch `needed` amount of pictures, ensuring it's not larger than 30 per page
            params = {
                'query': search_term,
                'per_page': min(needed + 5, 30), # Fetch a few extra in case we skip some
                'orientation': 'landscape',
                'content_filter': 'high',
            }
            
            response = requests.get(search_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                added = 0
                for i, photo in enumerate(results):
                    if added >= needed:
                        break
                        
                    image_url = photo['urls']['regular']
                    
                    # Generate a unique product name
                    prod_name = f"{random.choice(adjectives)} {category.name} #{i+1 + current_count}"
                    
                    # Create the product
                    Product.objects.create(
                        name=prod_name,
                        description=f"A fresh, high-quality {category.name.lower()} perfect for any occasion.",
                        price=round(random.uniform(5.99, 29.99), 2),
                        category=category,
                        seller=seller,
                        image=image_url[:500], # ensuring it fits in the max length we set earlier
                        stock=random.randint(5, 50)
                    )
                    added += 1
                    print(f"  ✅ Created: {prod_name}")
                
                if added < needed:
                    print(f"  ⚠️ Only found {added} images on Unsplash for {category.name}")
                    
            else:
                print(f"❌ API error for {category.name}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error for {category.name}: {str(e)}")
            
        # Avoid rate limits
        time.sleep(1)
        
    print("\n🎉 Product generation complete!")

if __name__ == "__main__":
    generate_products_for_categories()
