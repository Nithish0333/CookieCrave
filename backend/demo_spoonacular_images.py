"""
Demo script to show what Spoonacular API can provide for CookieCrave products
This shows sample image URLs and what you can expect from the API
"""

def show_spoonacular_examples():
    """Show example images that Spoonacular API provides"""
    
    print("🍪 CookieCrave - Spoonacular API Image Examples")
    print("=" * 55)
    
    # Example image URLs from Spoonacular (these are real examples)
    examples = {
        "Chocolate Chip Cookies": [
            "https://spoonacular.com/cdn/ingredients_100x100/chocolate-chip-cookies.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/cookies.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/chocolate-chips.jpg"
        ],
        "Chocolate Cake": [
            "https://spoonacular.com/cdn/ingredients_100x100/chocolate-cake.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/cake.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/chocolate.jpg"
        ],
        "Vanilla Milkshake": [
            "https://spoonacular.com/cdn/ingredients_100x100/vanilla-ice-cream.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/milkshake.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/vanilla.jpg"
        ],
        "Dark Chocolate Bar": [
            "https://spoonacular.com/cdn/ingredients_100x100/dark-chocolate.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/chocolate-bar.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/chocolate.jpg"
        ],
        "Almond Cookies": [
            "https://spoonacular.com/cdn/ingredients_100x100/almonds.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/cookies.jpg",
            "https://spoonacular.com/cdn/ingredients_100x100/almond.jpg"
        ]
    }
    
    for product_name, image_urls in examples.items():
        print(f"\n📸 {product_name}:")
        for i, url in enumerate(image_urls, 1):
            # Convert to high-res version
            high_res_url = url.replace('ingredients_100x100', 'ingredients_500x500')
            print(f"  {i}. {high_res_url}")
    
    print("\n" + "=" * 55)
    print("📋 API Benefits:")
    print("✅ High-quality food images (500x500 pixels)")
    print("✅ Professional food photography")
    print("✅ Consistent image style")
    print("✅ Free tier: 150 requests/day")
    print("✅ Easy integration with Django")
    
    print("\n🔧 Setup Instructions:")
    print("1. Visit: https://spoonacular.com/food-api")
    print("2. Sign up for free account")
    print("3. Get your API key")
    print("4. Add to .env: SPOONACULAR_API_KEY=your-key-here")
    print("5. Run: python fetch_spoonacular_images.py")
    
    print("\n📊 What the script does:")
    print("• Maps your products to search terms")
    print("• Fetches best matching images")
    print("• Updates product.image field in database")
    print("• Handles rate limiting and errors")
    print("• Provides detailed progress reporting")

def show_product_mapping():
    """Show how your products map to search terms"""
    
    print("\n🗂️ Product to Search Term Mapping:")
    print("=" * 40)
    
    mapping = {
        'Classic Chocolate Chip Cookies': 'chocolate chip cookies',
        'Double Chocolate Chip': 'double chocolate chip cookies',
        'White Chocolate Chip': 'white chocolate chip cookies',
        'Chocolate Cake Slice': 'chocolate cake slice',
        'Vanilla Cake': 'vanilla cake',
        'Strawberry Cake': 'strawberry cake',
        'Chocolate Milkshake': 'chocolate milkshake',
        'Vanilla Milkshake': 'vanilla milkshake',
        'Strawberry Milkshake': 'strawberry milkshake',
        'Dark Chocolate Bar': 'dark chocolate bar',
        'Milk Chocolate Bar': 'milk chocolate bar',
        'Chocolate Truffles': 'chocolate truffles',
        'Almond Cookies': 'almond cookies',
        'Cranberry Cookies': 'cranberry cookies',
        'Walnut Cookies': 'walnut cookies',
        'Oatmeal Raisin Cookies': 'oatmeal raisin cookies',
        'Oatmeal Honey Cookies': 'oatmeal honey cookies',
        'Oatmeal Cranberry Cookies': 'oatmeal cranberry cookies',
    }
    
    for product, search_term in mapping.items():
        print(f"🍪 {product}")
        print(f"   🔍 Searches: '{search_term}'")
        print()

if __name__ == "__main__":
    show_spoonacular_examples()
    show_product_mapping()
