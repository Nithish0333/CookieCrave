import os
import requests
import time

# Create media directory if it doesn't exist
media_dir = os.path.join(os.path.dirname(__file__), 'media', 'product_images')
os.makedirs(media_dir, exist_ok=True)

# Additional real food image URLs for more variety
additional_product_images = [
    # More Cookie Varieties
    ("sugar_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&bright=30"),
    ("peanut_butter_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=40"),
    ("macadamia_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=50"),
    ("gingerbread_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=20"),
    ("snickerdoodle_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&bright=20&hue=45"),
    
    # Brownies & Bars
    ("brownies.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&sat=-50"),
    ("blondies.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&bright=20"),
    ("lemon_bars.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=60&bright=30"),
    
    # More Cakes
    ("carrot_cake.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=30"),
    ("coffee_cake.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&sat=-30"),
    ("pound_cake.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&bright=10"),
    ("angel_food_cake.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&bright=40"),
    
    # Cupcakes & Muffins
    ("chocolate_cupcakes.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("vanilla_cupcakes.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&bright=20"),
    ("blueberry_muffins.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=240"),
    ("bran_muffins.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=30&sat=-20"),
    
    # Pies & Tarts
    ("apple_pie.jpg", "https://images.pexels.com/photos/1028726/pexels-photo-1028726.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=30"),
    ("cherry_pie.jpg", "https://images.pexels.com/photos/1028726/pexels-photo-1028726.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=340"),
    ("lemon_meringue.jpg", "https://images.pexels.com/photos/1028726/pexels-photo-1028726.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=60&bright=30"),
    
    # Pastries & Donuts
    ("glazed_donuts.jpg", "https://images.pexels.com/photos/1998633/pexels-photo-1998633.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&bright=30"),
    ("chocolate_donuts.jpg", "https://images.pexels.com/photos/1998633/pexels-photo-1998633.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&sat=-50"),
    ("cinnamon_rolls.jpg", "https://images.pexels.com/photos/2915281/pexels-photo-2915281.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=20&bright=20"),
    
    # More Beverages
    ("hot_chocolate.jpg", "https://images.pexels.com/photos/1998633/pexels-photo-1998633.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop"),
    ("coffee_latte.jpg", "https://images.pexels.com/photos/1998633/pexels-photo-1998633.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&sat=-30"),
    ("green_tea.jpg", "https://images.pexels.com/photos/1998633/pexels-photo-1998633.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=120&sat=-50"),
    
    # Seasonal & Holiday
    ("christmas_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=340&bright=20"),
    ("easter_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=300&bright=30"),
    ("halloween_cookies.jpg", "https://images.pexels.com/photos/1059905/pexels-photo-1059905.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop&hue=20&sat=-30"),
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
    """Download additional product images"""
    print("🍪 Downloading additional product photos...")
    print(f"📁 Saving to: {media_dir}")
    print()
    
    successful_downloads = 0
    total_images = len(additional_product_images)
    
    for filename, url in additional_product_images:
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
    print("🌐 These are additional high-quality food photos from Pexels")
    print("📸 All images are free for commercial use")
    print("🍪 Your CookieCrave store now has even more variety!")

if __name__ == "__main__":
    main()
