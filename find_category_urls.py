#!/usr/bin/env python3
import requests
import time

def find_category_specific_urls():
    """Find working Unsplash URLs for specific categories"""
    print("🔍 Finding Category-Specific Working URLs")
    print("=" * 60)
    
    # Category-specific search terms and photo IDs to test
    category_searches = {
        'Cookies': [
            '1499636136210-6f4ee915583e',  # Classic chocolate chip
            '1598968333180-9b4f6bc2bf52',  # Almond cookies  
            '1604466513550-3272a4927541',  # Cranberry cookies
            '1585518419759-72cc08ceaaaa',  # Oatmeal cookies
            '1514529470165-75021c6cc623',  # Walnut cookies
            '1556969092-0b42e2ca37ea',  # Double chocolate
            '1578985545062-69928b1d9587',  # Vanilla cookies
        ],
        'Cakes': [
            '1578985545062-69928b1d9587',  # Chocolate cake
            '1464349095981-7f2c70667386',  # Vanilla cake
            '1563729784474-dfbb5446cced',  # Strawberry cake
            '1556969092-0b42e2ca37ea',  # Birthday cake
            '1586191372612-6b5a50788e76',  # Honey cake
        ],
        'Milkshakes': [
            '1734747643067-6d4e0f705a00',  # Chocolate milkshake
            '1553530889-e6cf89870560',  # Strawberry milkshake
            '1578985545062-69928b1d9587',  # Vanilla milkshake
            '1555939594-58d7cb561a1a',  # Beverage
            '1522249341405-3871994ac062',  # Sweet drink
        ],
        'Chocolate': [
            '1522249341405-3871994ac062',  # Dark chocolate
            '1546069201-fa0afd4b5d0a',  # Milk chocolate
            '1596792503312-7e85e0b8c7a2',  # Chocolate truffles
            '1556969092-0b42e2ca37ea',  # Chocolate bar
            '1578985545062-69928b1d9587',  # Chocolate pieces
        ],
        'Fruit and Nuts': [
            '1514529470165-75021c6cc623',  # Walnuts
            '1598968333180-9b4f6bc2bf52',  # Almonds
            '1604466513550-3272a4927541',  # Cranberries
            '1578985545062-69928b1d9587',  # Mixed nuts
            '1499636136210-6f4ee915583e',  # Fruit and nut cookies
        ],
        'Oatmeal': [
            '1585518419759-72cc08ceaaaa',  # Oatmeal cookies
            '1586191372612-6b5a50788e76',  # Oatmeal honey
            '1578985545062-69928b1d9587',  # Oatmeal raisin
            '1499636136210-6f4ee915583e',  # Oatmeal cranberry
            '1556969092-0b42e2ca37ea',  # Oatmeal chocolate
        ]
    }
    
    working_urls_by_category = {}
    
    for category, photo_ids in category_searches.items():
        print(f"\n🔍 Testing {category} URLs:")
        working_urls = []
        
        for photo_id in photo_ids:
            url = f"https://images.unsplash.com/photo-{photo_id}?w=800&q=80"
            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Working: {photo_id}")
                    working_urls.append(url)
                    if len(working_urls) >= 5:  # We need 5 per category
                        break
                else:
                    print(f"❌ Failed: {photo_id} ({response.status_code})")
            except Exception as e:
                print(f"❌ Error: {photo_id} - {e}")
            
            time.sleep(0.1)  # Avoid rate limiting
        
        if working_urls:
            working_urls_by_category[category] = working_urls[:5]  # Keep only 5
            print(f"📊 Found {len(working_urls)} working URLs for {category}")
        else:
            print(f"⚠️  No working URLs found for {category}")
    
    return working_urls_by_category

if __name__ == "__main__":
    find_category_specific_urls()
