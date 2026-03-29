#!/usr/bin/env python
"""
Script to create placeholder images for products
Run this from the backend directory: python create_placeholder_images.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create media/product_images directory if it doesn't exist
os.makedirs('media/product_images', exist_ok=True)

# Define products with their colors and names
products = [
    # Chocolate Chip
    {'name': 'chocolate_chip_cookies.jpg', 'color': '#8B4513', 'text': '🍪\nChocolate Chip'},
    {'name': 'double_chocolate_chip.jpg', 'color': '#654321', 'text': '🍪\nDouble Chocolate'},
    {'name': 'white_chocolate_chip.jpg', 'color': '#D2B48C', 'text': '🍪\nWhite Chocolate'},
    
    # Cakes
    {'name': 'chocolate_cake.jpg', 'color': '#3D2817', 'text': '🎂\nChocolate Cake'},
    {'name': 'vanilla_cake.jpg', 'color': '#F5DEB3', 'text': '🎂\nVanilla Cake'},
    {'name': 'strawberry_cake.jpg', 'color': '#FFB6C1', 'text': '🎂\nStrawberry Cake'},
    
    # Milkshakes
    {'name': 'chocolate_milkshake.jpg', 'color': '#8B4513', 'text': '🥤\nChocolate Shake'},
    {'name': 'vanilla_milkshake.jpg', 'color': '#F5DEB3', 'text': '🥤\nVanilla Shake'},
    {'name': 'strawberry_milkshake.jpg', 'color': '#FFB6C1', 'text': '🥤\nStrawberry Shake'},
    
    # Chocolates
    {'name': 'dark_chocolate.jpg', 'color': '#2F1B0C', 'text': '🍫\nDark Chocolate'},
    {'name': 'milk_chocolate.jpg', 'color': '#8B4513', 'text': '🍫\nMilk Chocolate'},
    {'name': 'chocolate_truffles.jpg', 'color': '#654321', 'text': '🍫\nTruffles'},
    
    # Fruit and Nuts
    {'name': 'almond_cookies.jpg', 'color': '#D2B48C', 'text': '🥜\nAlmond Cookies'},
    {'name': 'cranberry_cookies.jpg', 'color': '#DC143C', 'text': '🍓\nCranberry Cookies'},
    {'name': 'walnut_cookies.jpg', 'color': '#8B7355', 'text': '🥜\nWalnut Cookies'},
    
    # Oatmeal
    {'name': 'oatmeal_raisin.jpg', 'color': '#CD853F', 'text': '🌾\nOatmeal Raisin'},
    {'name': 'oatmeal_honey.jpg', 'color': '#DAA520', 'text': '🌾\nOatmeal Honey'},
    {'name': 'oatmeal_cranberry.jpg', 'color': '#B8860B', 'text': '🌾\nOatmeal Cranberry'},
]

# Create images
for product in products:
    # Create a new image with the specified color
    img = Image.new('RGB', (400, 300), color=product['color'])
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Draw text in the center
    text = product['text']
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (400 - text_width) // 2
    y = (300 - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font, align='center')
    
    # Save the image
    img.save(f'media/product_images/{product["name"]}')
    print(f'Created: media/product_images/{product["name"]}')

print('\nAll placeholder images created successfully!')
