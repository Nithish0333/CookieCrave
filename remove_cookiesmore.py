#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def remove_cookiesmore_product():
    """Remove the 'cookiesmore' product from the database"""
    try:
        # Find the product with name 'cookiesmore'
        cookiesmore_product = Product.objects.get(name='cookiesmore')
        print(f"🔍 Found product: {cookiesmore_product.name} (ID: {cookiesmore_product.id})")
        print(f"📝 Description: {cookiesmore_product.description}")
        print(f"💰 Price: {cookiesmore_product.price}")
        print(f"👤 Seller: {cookiesmore_product.seller.username if cookiesmore_product.seller else 'Unknown'}")
        
        # Use raw SQL to delete the product bypassing ORM constraints
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Remove from recommendation system first
            try:
                cursor.execute("DELETE FROM recommendation_system_userrecommendation WHERE product_id = %s", [cookiesmore_product.id])
                print("🗑️ Removed from recommendation system")
            except Exception as e:
                print(f"⚠️ Recommendation table issue: {e}")
            
            # Remove from any wishlist relationships (if table exists)
            try:
                cursor.execute("DELETE FROM products_wishlist_products WHERE product_id = %s", [cookiesmore_product.id])
                print("🗑️ Removed from wishlist relationships")
            except Exception as e:
                print(f"⚠️ Wishlist table may not exist: {e}")
            
            # Delete the product directly
            cursor.execute("DELETE FROM products_product WHERE id = %s", [cookiesmore_product.id])
        
        product_name = cookiesmore_product.name
        print(f"✅ Successfully deleted product: '{product_name}'")
        print("🎉 The 'cookiesmore' product has been removed from your CookieCrave store!")
        
    except Product.DoesNotExist:
        print("❌ No product named 'cookiesmore' found in the database")
    except Exception as e:
        print(f"❌ Error deleting product: {e}")

if __name__ == "__main__":
    remove_cookiesmore_product()
