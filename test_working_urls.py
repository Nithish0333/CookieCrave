#!/usr/bin/env python3
import requests

def test_verified_urls():
    print("🔍 Testing All Unsplash URLs")
    print("=" * 50)
    
    urls_to_test = [
        'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
        'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=800&q=80',
        'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
        'https://images.unsplash.com/photo-1464349095981-7f2c70667386?w=800&q=80',
        'https://images.unsplash.com/photo-1734747643067-6d4e0f705a00?w=800&q=80',
        'https://images.unsplash.com/photo-1553530889-e6cf89870560?w=800&q=80',
        'https://images.unsplash.com/photo-1522249341405-3871994ac062?w=800&q=80',
        'https://images.unsplash.com/photo-1546069201-fa0afd4b5d0a?w=800&q=80',
        'https://images.unsplash.com/photo-1596792503312-7e85e0b8c7a2?w=800&q=80',
        'https://images.unsplash.com/photo-1556969092-0b42e2ca37ea?w=800&q=80',
        'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
        'https://images.unsplash.com/photo-1514529470165-75021c6cc623?w=800&q=80',
    ]
    
    working_urls = []
    
    for i, url in enumerate(urls_to_test, 1):
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ URL {i}: Working")
                working_urls.append(url)
            else:
                print(f"❌ URL {i}: Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ URL {i}: Error - {e}")
    
    print(f"\n📊 Found {len(working_urls)} working URLs out of {len(urls_to_test)}")
    
    if working_urls:
        print("\n✅ Working URLs:")
        for url in working_urls:
            print(f"   {url}")
    
    return working_urls

if __name__ == "__main__":
    test_verified_urls()
