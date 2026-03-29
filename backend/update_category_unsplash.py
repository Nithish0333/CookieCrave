import os
import django
import requests
import json
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Category

def update_category_images():
    access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    if not access_key or access_key == 'your-unsplash-access-key-here':
        print("❌ Please set your Unsplash Access Key in .env file")
        return
        
    print("📸 Fetching category images from Unsplash API...")
    
    updated_count = 0
    failed_count = 0
    
    for category in Category.objects.all():
        category_name = category.name
        
        try:
            search_url = "https://api.unsplash.com/search/photos"
            headers = {
                'Authorization': f'Client-ID {access_key}'
            }
            # Enhance search term for better food pictures
            search_term = f"{category_name.lower()} dessert food"
            params = {
                'query': search_term,
                'per_page': 1,
                'orientation': 'landscape',
                'content_filter': 'high',
            }
            
            print(f"🔍 Searching Unsplash for: {search_term}")
            response = requests.get(search_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('results') and len(data['results']) > 0:
                    photo = data['results'][0]
                    # Use a smaller crop for categories
                    image_url = photo['urls']['regular']
                    
                    category.image_url = image_url
                    category.save()
                    updated_count += 1
                    print(f"✅ Updated {category_name}")
                else:
                    print(f"⚠️ No results found for {category_name}")
                    # Try a fallback if no results
                    fallback_term = "dessert pastry"
                    params['query'] = fallback_term
                    resp_fallback = requests.get(search_url, headers=headers, params=params, timeout=10)
                    if resp_fallback.status_code == 200 and resp_fallback.json().get('results'):
                        category.image_url = resp_fallback.json()['results'][0]['urls']['regular']
                        category.save()
                        updated_count += 1
                        print(f"✅ Updated {category_name} with fallback image")
                    else:
                        failed_count += 1
                        
            else:
                print(f"❌ API error for {category_name}: {response.status_code}")
                failed_count += 1
                
        except Exception as e:
            print(f"❌ Error fetching image for {category_name}: {str(e)}")
            failed_count += 1
    
    print(f"\n📊 Summary: Updated {updated_count} categories. Failed {failed_count}.")

if __name__ == "__main__":
    update_category_images()
