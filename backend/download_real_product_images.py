import os
import requests
from urllib.parse import urlparse
import time

# Create media directory if it doesn't exist
media_dir = os.path.join(os.path.dirname(__file__), 'media', 'product_images')
os.makedirs(media_dir, exist_ok=True)

# Real product image URLs (high-quality cookie and dessert photos)
real_product_images = [
    # Chocolate Cookies
    ("chocolate_chip_cookies.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center"),
    ("double_chocolate_chip.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center&sat=-100"),
    ("dark_chocolate.jpg", "https://images.unsplash.com/photo-1481391319762-471ff1b53056?w=400&h=300&fit=crop&crop=center"),
    ("milk_chocolate.jpg", "https://images.unsplash.com/photo-1481391319762-471ff1b53056?w=400&h=300&fit=crop&crop=center&sat=-50"),
    ("chocolate_truffles.jpg", "https://images.unsplash.com/photo-1486427935298-d91fdc2a79a6?w=400&h=300&fit=crop&crop=center"),
    
    # Vanilla & Light Cookies
    ("vanilla_cake.jpg", "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center"),
    ("white_chocolate_chip.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center&bright=20"),
    ("almond_cookies.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center&hue=30"),
    
    # Berry & Fruit Cookies
    ("cranberry_cookies.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center&hue=340"),
    ("strawberry_cake.jpg", "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center&hue=340"),
    ("strawberry_milkshake.jpg", "https://images.unsplash.com/photo-1565909532043-b37f5ad60d81?w=400&h=300&fit=crop&crop=center"),
    
    # Cakes & Desserts
    ("chocolate_cake.jpg", "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center"),
    ("red_velvet_cake.jpg", "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop&crop=center&hue=0"),
    ("cheesecake.jpg", "https://images.unsplash.com/photo-1565958016938-9e3de6e7e2b2?w=400&h=300&fit=crop&crop=center"),
    ("chocolate_lava_cake.jpg", "https://images.unsplash.com/photo-1565958016938-9e3de6e7e2b2?w=400&h=300&fit=crop&crop=center&sat=-50"),
    
    # Oatmeal & Healthy Options
    ("oatmeal_raisin.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center&hue=30&sat=-30"),
    ("oatmeal_honey.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center&hue=45&sat=-20"),
    ("oatmeal_cranberry.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center&hue=340&sat=-30"),
    ("walnut_cookies.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center&hue=25&sat=-40"),
    
    # Milkshakes & Drinks
    ("vanilla_milkshake.jpg", "https://images.unsplash.com/photo-1565909532043-b37f5ad60d81?w=400&h=300&fit=crop&crop=center&bright=10"),
    ("chocolate_milkshake.jpg", "https://images.unsplash.com/photo-1565909532043-b37f5ad60d81?w=400&h=300&fit=crop&crop=center&sat=-50"),
    
    # Test/Default
    ("testcookie.jpg", "https://images.unsplash.com/photo-1505252585461-04db1eb54687?w=400&h=300&fit=crop&crop=center")
]

def download_image(filename, url):
    """Download an image from URL and save it locally"""
    try:
        # Add user agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        filepath = os.path.join(media_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        file_size = os.path.getsize(filepath)
        print(f"✅ Downloaded: {filename} ({file_size} bytes)")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error saving {filename}: {e}")
        return False

def main():
    """Download all real product images"""
    print("🍪 Downloading real product images...")
    print(f"📁 Saving to: {media_dir}")
    print()
    
    successful_downloads = 0
    total_images = len(real_product_images)
    
    for filename, url in real_product_images:
        print(f"📥 Downloading: {filename}")
        if download_image(filename, url):
            successful_downloads += 1
        
        # Add a small delay to be respectful to the image service
        time.sleep(0.5)
    
    print()
    print(f"🎉 Download complete!")
    print(f"✅ Successfully downloaded: {successful_downloads}/{total_images} images")
    print(f"📂 Images saved in: {media_dir}")
    print()
    print("🌐 These are real, high-quality photos from Unsplash")
    print("📸 All images are free for commercial use")
    print("🍪 Your products now have realistic, appetizing photos!")

if __name__ == "__main__":
    main()
