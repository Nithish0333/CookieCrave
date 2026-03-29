#!/usr/bin/env python
"""
EASY MANUAL IMAGE UPLOAD
Step-by-step guide to add unique images manually
"""
import os
import sys
import requests
from io import BytesIO
from PIL import Image
import django

# Setup Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def easy_manual_upload():
    print("🖼️  EASY MANUAL IMAGE UPLOAD")
    print("=" * 50)
    
    # Show products that need images
    products_needing_images = Product.objects.filter(image_data__isnull=True).order_by('name')
    
    print(f"\n📋 Products needing images: {len(products_needing_images)}")
    print("   (These are the ones showing repetitive images)")
    
    # Show first 10 products
    for i, product in enumerate(products_needing_images[:10], 1):
        print(f"   {i:2}. {product.name}")
    
    if len(products_needing_images) > 10:
        print(f"   ... and {len(products_needing_images) - 10} more")
    
    print(f"\n🎯 HOW TO ADD IMAGES MANUALLY:")
    print(f"   1. Choose a product from the list")
    print(f"   2. Find a good image URL")
    print(f"   3. I'll download and store it")
    print(f"   4. Repeat until all products have images")
    
    print(f"\n📱 BEST PLACES TO FIND IMAGES:")
    print(f"   • Unsplash.com - Search 'chocolate chip cookies'")
    print(f"   • Pexels.com - Search 'cake slice'")
    print(f"   • Pixabay.com - Search 'milkshake'")
    
    # Interactive upload loop
    while products_needing_images.exists():
        print(f"\n" + "="*60)
        
        # Show current status
        remaining = products_needing_images.count()
        completed = Product.objects.filter(image_data__isnull=False).count()
        total = Product.objects.count()
        
        print(f"📊 Progress: {completed}/{total} completed, {remaining} remaining")
        
        # Show next 5 products
        next_products = products_needing_images[:5]
        print(f"\n🍪 Next products needing images:")
        for i, product in enumerate(next_products, 1):
            print(f"   {i}. {product.name}")
        
        try:
            choice = input(f"\nSelect product (1-{len(next_products)}) or 'quit': ").strip()
            
            if choice.lower() == 'quit':
                break
            
            choice_num = int(choice)
            if choice_num < 1 or choice_num > len(next_products):
                print(f"❌ Invalid choice")
                continue
            
            product = next_products[choice_num - 1]
            print(f"\n🍪 Selected: {product.name}")
            
            # Get image URL
            print(f"\n📱 Find an image for '{product.name}':")
            print(f"   1. Go to Unsplash.com")
            print(f"   2. Search for: '{product.name}'")
            print(f"   3. Click on a good image")
            print(f"   4. Right-click → 'Copy Image Address'")
            
            image_url = input(f"\n📥 Paste the image URL: ").strip()
            
            if not image_url:
                print(f"❌ No URL provided")
                continue
            
            # Test and download the image
            print(f"   🔍 Testing URL...")
            try:
                response = requests.head(image_url, timeout=5)
                if response.status_code != 200:
                    print(f"❌ URL not accessible (status: {response.status_code})")
                    continue
                
                print(f"   ✅ URL accessible")
                
                # Download and process
                print(f"   📥 Downloading image...")
                response = requests.get(image_url, timeout=15)
                response.raise_for_status()
                
                img = Image.open(BytesIO(response.content))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=85, optimize=True)
                image_data = buffer.getvalue()
                
                # Store in database
                product.image_data = image_data
                product.image_url = image_url
                product.save()
                
                print(f"   ✅ SUCCESS! Image stored ({len(image_data)} bytes)")
                print(f"   🗄️  Now stored in PostgreSQL database")
                
                # Refresh the list
                products_needing_images = Product.objects.filter(image_data__isnull=True).order_by('name')
                
                if not products_needing_images.exists():
                    print(f"\n🎉 ALL DONE! All products now have unique images!")
                    break
                    
            except requests.RequestException as e:
                print(f"❌ Network error: {e}")
            except Exception as e:
                print(f"❌ Error processing image: {e}")
                
        except ValueError:
            print(f"❌ Please enter a valid number")
        except KeyboardInterrupt:
            print(f"\n👋 Goodbye!")
            break
    
    # Final status
    total_products = Product.objects.count()
    products_with_images = Product.objects.filter(image_data__isnull=False).count()
    
    print(f"\n📊 FINAL STATUS:")
    print(f"   Total products: {total_products}")
    print(f"   With unique images: {products_with_images}")
    print(f"   Still needed: {total_products - products_with_images}")
    
    if products_with_images == total_products:
        print(f"\n🎉 PERFECT! Zero repetitive images!")
        print(f"   All {total_products} products have unique PostgreSQL images")
    else:
        print(f"\n🔄 Keep going! Only {total_products - products_with_images} more to go")

def show_quick_tips():
    print("💡 QUICK TIPS FOR BEST RESULTS:")
    print("=" * 40)
    print("✅ Choose high-quality, clear images")
    print("✅ Make sure images match the product name")
    print("✅ Use consistent lighting and style")
    print("✅ Avoid images with watermarks")
    print("✅ Test URLs before pasting them")
    print("✅ Be patient - downloads can take time")

if __name__ == "__main__":
    print("🖼️  MANUAL IMAGE UPLOAD SYSTEM")
    print("This will eliminate ALL repetitive images!")
    print("")
    print("Choose an option:")
    print("1. Start adding images manually")
    print("2. Show quick tips")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        easy_manual_upload()
    elif choice == "2":
        show_quick_tips()
    else:
        print("❌ Invalid choice")
