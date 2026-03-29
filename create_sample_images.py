import os
from PIL import Image, ImageDraw, ImageFont
import random

# Create media directory if it doesn't exist
media_dir = os.path.join(os.path.dirname(__file__), 'media', 'product_images')
os.makedirs(media_dir, exist_ok=True)

# Sample product names and colors
products = [
    ("vanilla_milkshake.jpg", "#FFE4B5", "Vanilla Milkshake"),
    ("strawberry_milkshake.jpg", "#FFB6C1", "Strawberry Milkshake"),
    ("chocolate_lava_cake.jpg", "#8B4513", "Chocolate Lava Cake"),
    ("red_velvet_cake.jpg", "#8B0000", "Red Velvet Cake"),
    ("cheesecake.jpg", "#FFF8DC", "Cheesecake"),
    ("dark_chocolate.jpg", "#654321", "Dark Chocolate"),
    ("milk_chocolate.jpg", "#D2691E", "Milk Chocolate"),
    ("chocolate_truffles.jpg", "#4B3621", "Chocolate Truffles"),
    ("almond_cookies.jpg", "#F4E4C1", "Almond Cookies"),
    ("cranberry_cookies.jpg", "#DC143C", "Cranberry Cookies"),
    ("chocolate_chip_cookies.jpg", "#8B4513", "Chocolate Chip Cookies"),
    ("double_chocolate_chip.jpg", "#654321", "Double Chocolate Chip"),
    ("white_chocolate_chip.jpg", "#FFF8DC", "White Chocolate Chip"),
    ("chocolate_cake.jpg", "#8B4513", "Chocolate Cake"),
    ("vanilla_cake.jpg", "#FFF8DC", "Vanilla Cake"),
    ("strawberry_cake.jpg", "#FFB6C1", "Strawberry Cake"),
    ("chocolate_milkshake.jpg", "#8B4513", "Chocolate Milkshake"),
    ("walnut_cookies.jpg", "#8B7355", "Walnut Cookies"),
    ("oatmeal_raisin.jpg", "#D2691E", "Oatmeal Raisin"),
    ("oatmeal_honey.jpg", "#DEB887", "Oatmeal Honey"),
    ("oatmeal_cranberry.jpg", "#CD853F", "Oatmeal Cranberry"),
    ("testcookie.jpg", "#8B4513", "Test Cookie")
]

def create_cookie_image(filename, bg_color, product_name):
    """Create a simple cookie image with text"""
    width, height = 400, 300
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a circle to represent a cookie
    cookie_color = "#D2691E" if "chocolate" in product_name.lower() else "#F4E4C1"
    draw.ellipse([50, 50, 350, 250], fill=cookie_color)
    
    # Draw some chocolate chips or decorations
    chip_color = "#654321" if "chocolate" in product_name.lower() else "#8B4513"
    for _ in range(8):
        x = random.randint(80, 320)
        y = random.randint(80, 220)
        r = random.randint(5, 15)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=chip_color)
    
    # Add text
    try:
        # Try to use a larger font
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text_lines = product_name.split()
    y_text = 20
    for line in text_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_text = (width - text_width) // 2
        draw.text((x_text, y_text), line, fill="white" if bg_color == "#8B4513" or bg_color == "#654321" else "black", font=font)
        y_text += 25
    
    # Save the image
    filepath = os.path.join(media_dir, filename)
    img.save(filepath)
    print(f"Created: {filepath}")

# Create all product images
for filename, color, name in products:
    create_cookie_image(filename, color, name)

print(f"\nCreated {len(products)} sample product images in {media_dir}")
print("Images are now ready to be displayed!")
