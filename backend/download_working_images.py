import os
import requests
import time

# Create media directory if it doesn't exist
media_dir = os.path.join(os.path.dirname(__file__), 'media', 'product_images')
os.makedirs(media_dir, exist_ok=True)

# Working real food image URLs (from various free stock photo sites)
working_product_images = [
    # Chocolate Cookies & Treats
    ("chocolate_chip_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("double_chocolate_chip.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("dark_chocolate.jpg", "https://images.pexels.com/photos/1998633/pexels-photo-1998633.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("milk_chocolate.jpg", "https://images.pexels.com/photos/1998633/pexels-photo-1998633.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("chocolate_truffles.jpg", "https://images.pexels.com/photos/1998633/pexels-photo-1998633.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    
    # Vanilla & Light Treats
    ("vanilla_cake.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("white_chocolate_chip.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("almond_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    
    # Berry & Fruit Treats
    ("cranberry_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("strawberry_cake.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("strawberry_milkshake.jpg", "https://images.pexels.com/photos/134469/pexels-photo-134469.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    
    # Cakes & Desserts
    ("chocolate_cake.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("red_velvet_cake.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("cheesecake.jpg", "https://images.pexels.com/photos/1028726/pexels-photo-1028726.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("chocolate_lava_cake.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    
    # Oatmeal & Healthy Options
    ("oatmeal_raisin.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("oatmeal_honey.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("oatmeal_cranberry.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("walnut_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    
    # Milkshakes & Drinks
    ("vanilla_milkshake.jpg", "https://images.pexels.com/photos/134469/pexels-photo-134469.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("chocolate_milkshake.jpg", "https://images.pexels.com/photos/134469/pexels-photo-134469.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    
    # Test/Default
    ("testcookie.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop")
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
    print("🍪 Downloading real product photos...")
    print(f"📁 Saving to: {media_dir}")
    print()
    
    successful_downloads = 0
    total_images = len(working_product_images)
    
    for filename, url in working_product_images:
        print(f"📥 Downloading: {filename}")
        if download_image(filename, url):
            successful_downloads += 1
        
        # Add a small delay to be respectful to the image service
        time.sleep(0.3)
    
    print()
    print(f"🎉 Download complete!")
    print(f"✅ Successfully downloaded: {successful_downloads}/{total_images} images")
    print(f"📂 Images saved in: {media_dir}")
    print()
    print("🌐 These are real, high-quality food photos from Pexels")
    print("📸 All images are free for commercial use")
    print("🍪 Your products now have realistic, appetizing photos!")

if __name__ == "__main__":
    main()
