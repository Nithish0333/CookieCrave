#!/usr/bin/env python
"""
Check What Products Still Need Images
Show you exactly what to add next
"""
import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def show_missing_products():
    print("📋 PRODUCTS THAT STILL NEED IMAGES")
    print("=" * 50)
    
    # Get all products
    all_products = Product.objects.all().order_by('name')
    
    # Current PRODUCT_IMAGES from manual_image_setup.py
    current_images = {
        'Classic Chocolate Chip Cookies', 'Double Chocolate Chip', 'White Chocolate Chip',
        'Almond Cookies', 'Cranberry Cookies', 'Walnut Cookies', 'Oatmeal Raisin Cookies',
        'Oatmeal Honey Cookies', 'Oatmeal Cranberry Cookies', 'Chocolate Cake Slice',
        'Vanilla Cake', 'Strawberry Cake', 'Chocolate Milkshake', 'Vanilla Milkshake',
        'Strawberry Milkshake', 'Dark Chocolate Bar', 'Milk Chocolate Bar', 'Chocolate Truffles'
    }
    
    print(f"✅ Already have images: {len(current_images)} products")
    print(f"📊 Total products in database: {all_products.count()}")
    
    # Show missing products
    missing_products = []
    for product in all_products:
        if product.name not in current_images:
            missing_products.append(product.name)
    
    print(f"\n🔍 MISSING PRODUCTS (need {len(missing_products)} more):")
    
    # Group by category
    cookies = []
    cakes = []
    milkshakes = []
    chocolates = []
    others = []
    
    for product_name in missing_products:
        name_lower = product_name.lower()
        if 'cookie' in name_lower or 'oatmeal' in name_lower:
            cookies.append(product_name)
        elif 'cake' in name_lower:
            cakes.append(product_name)
        elif 'milkshake' in name_lower:
            milkshakes.append(product_name)
        elif 'chocolate' in name_lower:
            chocolates.append(product_name)
        else:
            others.append(product_name)
    
    if cookies:
        print(f"\n🍪 COOKIES ({len(cookies)}):")
        for cookie in cookies:
            print(f"   - {cookie}")
    
    if cakes:
        print(f"\n🎂 CAKES ({len(cakes)}):")
        for cake in cakes:
            print(f"   - {cake}")
    
    if milkshakes:
        print(f"\n🥤 MILKSHAKES ({len(milkshakes)}):")
        for shake in milkshakes:
            print(f"   - {shake}")
    
    if chocolates:
        print(f"\n🍫 CHOCOLATES ({len(chocolates)}):")
        for choc in chocolates:
            print(f"   - {choc}")
    
    if others:
        print(f"\n🔄 OTHERS ({len(others)}):")
        for other in others:
            print(f"   - {other}")
    
    print(f"\n🎯 NEXT ACTION:")
    print(f"1. Add these {len(missing_products)} products to PRODUCT_IMAGES dictionary")
    print(f"2. Find unique image URLs for each")
    print(f"3. Run: python manual_image_setup.py")
    
    # Create the complete dictionary template
    print(f"\n📝 COPY THIS TO YOUR manual_image_setup.py:")
    print("PRODUCT_IMAGES = {")
    
    # Show existing ones
    existing_urls = {
        'Classic Chocolate Chip Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
        'Double Chocolate Chip': 'https://images.unsplash.com/photo-1556969092-0b42e2ca37ea?w=800&q=80',
        'White Chocolate Chip': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
        'Almond Cookies': 'https://images.unsplash.com/photo-1598968333180-9b4f6bc2bf52?w=800&q=80',
        'Cranberry Cookies': 'https://images.unsplash.com/photo-1604466513550-3272a4927541?w=800&q=80',
        'Walnut Cookies': 'https://images.unsplash.com/photo-1514529470165-75021c6cc623?w=800&q=80',
        'Oatmeal Raisin Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
        'Oatmeal Honey Cookies': 'https://images.unsplash.com/photo-1586191372612-6b5a50788e76?w=800&q=80',
        'Oatmeal Cranberry Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
        'Chocolate Cake Slice': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
        'Vanilla Cake': 'https://images.unsplash.com/photo-1464349095981-7f2c70667386?w=800&q=80',
        'Strawberry Cake': 'https://images.unsplash.com/photo-1563729784474-dfbb5446cced?w=800&q=80',
        'Chocolate Milkshake': 'https://images.unsplash.com/photo-1734747643067-6d4e0f705a00?w=800&q=80',
        'Vanilla Milkshake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
        'Strawberry Milkshake': 'https://images.unsplash.com/photo-1553530889-e6cf89870560?w=800&q=80',
        'Dark Chocolate Bar': 'https://images.unsplash.com/photo-1522249341405-3871994ac062?w=800&q=80',
        'Milk Chocolate Bar': 'https://images.unsplash.com/photo-1546069201-fa0afd4b5d0a?w=800&q=80',
        'Chocolate Truffles': 'https://images.unsplash.com/photo-1596792503312-7e85e0b8c7a2?w=800&q=80',
    }
    
    for name, url in existing_urls.items():
        print(f"    '{name}': '{url}',")
    
    # Add missing ones as template
    for product_name in missing_products:
        print(f"    '{product_name}': 'ADD_URL_HERE',")
    
    print("}")

if __name__ == "__main__":
    show_missing_products()
