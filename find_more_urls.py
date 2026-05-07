#!/usr/bin/env python3
import requests
import time

def find_more_working_urls():
    """Find more working Unsplash URLs by testing common photo IDs"""
    print("🔍 Finding More Working Unsplash URLs")
    print("=" * 50)
    
    # Common working Unsplash photo IDs to test
    photo_ids = [
        '1499636136210-6f4ee915583e',  # Classic working
        '1495521821757-a1efb6729352',  # Default working
        '1578985545062-69928b1d9587',  # Cake working
        '1734747643067-6d4e0f705a00',  # Milkshake working
        '1522249341405-3871994ac062',  # Chocolate working
        '1556969092-0b42e2ca37ea',  # Double chocolate
        '1585518419759-72cc08ceaaaa',  # Oatmeal
        '1514529470165-75021c6cc623',  # Walnut
        '1598968333180-9b4f6bc2bf52',  # Almond
        '1604466513550-3272a4927541',  # Cranberry
        '1464349095981-7f2c70667386',  # Vanilla cake
        '1563729784474-dfbb5446cced',  # Strawberry
        '1553530889-e6cf89870560',  # Strawberry milkshake
        '1546069201-fa0afd4b5d0a',  # Milk chocolate
        '1596792503312-7e85e0b8c7a2',  # Truffles
        '1586191372612-6b5a50788e76',  # Honey
        '1578985545062-69928b1d9587',  # Vanilla
        '1555939594-58d7cb561a1a',  # Beverage
        '1514529470165-75021c6cc623',  # Nuts
        '1522249341405-3871994ac062',  # Dark chocolate
    ]
    
    working_urls = []
    
    for photo_id in photo_ids:
        url = f"https://images.unsplash.com/photo-{photo_id}?w=800&q=80"
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Working: {photo_id}")
                working_urls.append(url)
            else:
                print(f"❌ Failed: {photo_id} ({response.status_code})")
        except Exception as e:
            print(f"❌ Error: {photo_id} - {e}")
        
        # Add small delay to avoid rate limiting
        time.sleep(0.1)
    
    print(f"\n📊 Found {len(working_urls)} working URLs")
    
    return working_urls

if __name__ == "__main__":
    find_more_working_urls()
