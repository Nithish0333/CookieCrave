#!/usr/bin/env python
"""
Complete Product Image Mapping
Add all your manually selected images here
"""

# COMPLETE PRODUCT IMAGE MAPPING
# Replace these URLs with your actual selected images
PRODUCT_IMAGES = {
    # COOKIES
    'Classic Chocolate Chip Cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80',
    'Double Chocolate Chip': 'https://images.unsplash.com/photo-1556969092-0b42e2ca37ea?w=800&q=80',
    'White Chocolate Chip': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Almond Cookies': 'https://images.unsplash.com/photo-1598968333180-9b4f6bc2bf52?w=800&q=80',
    'Cranberry Cookies': 'https://images.unsplash.com/photo-1604466513550-3272a4927541?w=800&q=80',
    'Walnut Cookies': 'https://images.unsplash.com/photo-1514529470165-75021c6cc623?w=800&q=80',
    'Oatmeal Raisin Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
    'Oatmeal Honey Cookies': 'https://images.unsplash.com/photo-1586191372612-6b5a50788e76?w=800&q=80',
    'Oatmeal Cranberry Cookies': 'https://images.unsplash.com/photo-1585518419759-72cc08ceaaaa?w=800&q=80',
    
    # CAKES
    'Chocolate Cake Slice': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Vanilla Cake': 'https://images.unsplash.com/photo-1464349095981-7f2c70667386?w=800&q=80',
    'Strawberry Cake': 'https://images.unsplash.com/photo-1563729784474-dfbb5446cced?w=800&q=80',
    
    # MILKSHAKES
    'Chocolate Milkshake': 'https://images.unsplash.com/photo-1734747643067-6d4e0f705a00?w=800&q=80',
    'Vanilla Milkshake': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Strawberry Milkshake': 'https://images.unsplash.com/photo-1553530889-e6cf89870560?w=800&q=80',
    
    # CHOCOLATES
    'Dark Chocolate Bar': 'https://images.unsplash.com/photo-1522249341405-3871994ac062?w=800&q=80',
    'Milk Chocolate Bar': 'https://images.unsplash.com/photo-1546069201-fa0afd4b5d0a?w=800&q=80',
    'Chocolate Truffles': 'https://images.unsplash.com/photo-1596792503312-7e85e0b8c7a2?w=800&q=80',
    
    # VARIANTS - Add your variant products here
    'Premium Chocolate Chip #4': 'https://images.unsplash.com/photo-1556969092-0b42e2ca37ea?w=800&q=80',
    'Artisan Chocolate Chip #5': 'https://images.unsplash.com/photo-1598968333180-9b4f6bc2bf52?w=800&q=80',
    'Ultimate Chocolate Chip #6': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&q=80',
    'Deluxe Chocolate Chip #9': 'https://images.unsplash.com/photo-1522249341405-3871994ac062?w=800&q=80',
    
    # Add all remaining products with their image URLs...
    # You need to find and add images for all 48 products
}

print("📝 PRODUCT_IMAGES Dictionary Ready!")
print(f"Defined images for {len(PRODUCT_IMAGES)} products")
print("\n🔧 Instructions:")
print("1. Copy this dictionary to manual_image_setup.py")
print("2. Replace URLs with your actual selected images")
print("3. Run: python manual_image_setup.py")
print("4. All images will be stored in PostgreSQL")

# Show missing products
import os
import sys
import django

backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

all_products = set(product.name for product in Product.objects.all())
defined_products = set(PRODUCT_IMAGES.keys())
missing_products = all_products - defined_products

if missing_products:
    print(f"\n⚠️  Missing images for {len(missing_products)} products:")
    for product in sorted(missing_products):
        print(f"   - {product}")
else:
    print(f"\n✅ All {len(all_products)} products have images defined!")
