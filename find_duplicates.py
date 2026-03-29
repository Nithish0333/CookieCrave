#!/usr/bin/env python
import requests

def find_duplicate_products():
    print("🔍 Finding Products with Duplicate Images")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:8000/api/products/', timeout=10)
        data = response.json()
        
        # Find which products share images
        image_to_products = {}
        
        for product in data:
            image_url = product.get('image', 'NO IMAGE')
            if image_url not in image_to_products:
                image_to_products[image_url] = []
            image_to_products[image_url].append(product)
        
        # Show duplicates
        duplicates_found = False
        for image_url, products in image_to_products.items():
            if len(products) > 1:
                duplicates_found = True
                print(f"\n❌ Duplicate Image ({len(products)} products):")
                print(f"   URL: {image_url}")
                print(f"   Products:")
                for product in products:
                    print(f"     - {product.get('name', 'Unknown')}")
        
        if not duplicates_found:
            print(f"\n🎉 SUCCESS! No duplicates found!")
            print(f"   All {len(data)} products have unique images")
        else:
            print(f"\n📊 Summary:")
            print(f"   Total products: {len(data)}")
            print(f"   Unique images: {len(image_to_products)}")
            print(f"   Duplicates: {sum(1 for products in image_to_products.values() if len(products) > 1)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    find_duplicate_products()
