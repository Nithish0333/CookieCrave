"""
Script to update product image fields in the database so they point
to the actual local image files in media/product_images/.
Run with: python fix_product_images.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# Map each product name to the correct local image filename
PRODUCT_IMAGE_MAP = {
    'Classic Chocolate Chip Cookies': 'classic_chocolate_chip_cookies.jpg',
    'Double Chocolate Chip': 'double_chocolate_chip.jpg',
    'White Chocolate Chip': 'white_chocolate_chip.jpg',
    'Chocolate Cake Slice': 'chocolate_cake_slice.jpg',
    'Vanilla Cake': 'vanilla_cake.jpg',
    'Strawberry Cake': 'strawberry_cake.jpg',
    'Chocolate Milkshake': 'chocolate_milkshake.jpg',
    'Vanilla Milkshake': 'vanilla_cupcakes.jpg',   # closest match
    'Strawberry Milkshake': 'strawberry_milkshake.jpg',
    'Dark Chocolate Bar': 'dark_chocolate.jpg',
    'Milk Chocolate Bar': 'milk_chocolate.jpg',
    'Chocolate Truffles': 'chocolate_truffles.jpg',
    'Almond Cookies': 'almond_cookies.jpg',
    'Cranberry Cookies': 'cranberry_cookies.jpg',
    'Walnut Cookies': 'peanut_butter_cookies.jpg',  # closest match
    'Oatmeal Raisin Cookies': 'oatmeal_raisin_cookies.jpg',
    'Oatmeal Honey Cookies': 'oatmeal_honey.jpg',
    'Oatmeal Cranberry Cookies': 'oatmeal_cranberry.jpg',
    # Extra images from disk mapped to common product names
    'Sugar Cookies': 'sugar_cookies.jpg',
    'Snickerdoodle Cookies': 'snickerdoodle_cookies.jpg',
    'Gingerbread Cookies': 'gingerbread_cookies.jpg',
    'Macadamia Cookies': 'macadamia_cookies.jpg',
    'Peanut Butter Cookies': 'peanut_butter_cookies.jpg',
    'Christmas Cookies': 'christmas_cookies.jpg',
    'Easter Cookies': 'easter_cookies.jpg',
    'Halloween Cookies': 'halloween_cookies.jpg',
    'Brownies': 'brownies.jpg',
    'Blondies': 'blondies.jpg',
    'Lemon Bars': 'lemon_bars.jpg',
    'Cheesecake': 'cheesecake.jpg',
    'Red Velvet Cake': 'red_velvet_cake.jpg',
    'Carrot Cake': 'carrot_cake.jpg',
    'Coffee Cake': 'coffee_cake.jpg',
    'Pound Cake': 'pound_cake.jpg',
    'Angel Food Cake': 'angel_food_cake.jpg',
    'Chocolate Lava Cake': 'chocolate_lava_cake.jpg',
    'Vanilla Cupcakes': 'vanilla_cupcakes.jpg',
    'Chocolate Cupcakes': 'chocolate_cupcakes.jpg',
    'Blueberry Muffins': 'blueberry_muffins.jpg',
    'Bran Muffins': 'bran_muffins.jpg',
    'Cinnamon Rolls': 'cinnamon_rolls.jpg',
    'Glazed Donuts': 'glazed_donuts.jpg',
    'Chocolate Donuts': 'chocolate_donuts.jpg',
    'Apple Pie': 'apple_pie.jpg',
    'Cherry Pie': 'cherry_pie.jpg',
    'Lemon Meringue': 'lemon_meringue.jpg',
    'Hot Chocolate': 'hot_chocolate.jpg',
    'Coffee Latte': 'coffee_latte.jpg',
    'Green Tea': 'green_tea.jpg',
}

media_root = os.path.join(os.path.dirname(__file__), 'media')
products = Product.objects.all()
updated = 0
skipped = 0

for product in products:
    matched = None
    # Direct name match
    if product.name in PRODUCT_IMAGE_MAP:
        matched = PRODUCT_IMAGE_MAP[product.name]
    else:
        # Fuzzy match: check if any key is a substring of the product name or vice versa
        name_lower = product.name.lower()
        for key, val in PRODUCT_IMAGE_MAP.items():
            if key.lower() in name_lower or name_lower in key.lower():
                matched = val
                break
        # Try matching by individual words
        if not matched:
            words = name_lower.split()
            for key, val in PRODUCT_IMAGE_MAP.items():
                key_lower = key.lower()
                if any(w in key_lower for w in words if len(w) > 4):
                    matched = val
                    break

    if matched:
        full_path = os.path.join(media_root, 'product_images', matched)
        if os.path.exists(full_path):
            image_field_value = f'product_images/{matched}'
            product.image = image_field_value
            product.save(update_fields=['image'])
            print(f"[OK] Updated: {product.name!r} -> {image_field_value}")
            updated += 1
        else:
            print(f"[WARN] File not found for {product.name!r}: {full_path}")
            skipped += 1
    else:
        # Try to find any matching image by product name words
        name_words = product.name.lower().replace(' ', '_')
        # Check all image files
        img_dir = os.path.join(media_root, 'product_images')
        best_match = None
        for fname in os.listdir(img_dir):
            fname_base = fname.replace('.jpg', '').replace('.png', '')
            if fname_base in name_words or name_words in fname_base:
                best_match = fname
                break
        if best_match:
            product.image = f'product_images/{best_match}'
            product.save(update_fields=['image'])
            print(f"[OK] Auto-matched: {product.name!r} -> product_images/{best_match}")
            updated += 1
        else:
            # Use chocolate_chip as default for cookies
            default_img = 'chocolate_chip_cookies.jpg'
            if 'cookie' in product.name.lower() or 'Cookie' in product.name:
                default_img = 'chocolate_chip_cookies.jpg'
            elif 'cake' in product.name.lower():
                default_img = 'chocolate_cake.jpg'
            elif 'chocolate' in product.name.lower():
                default_img = 'chocolate_truffles.jpg'
            product.image = f'product_images/{default_img}'
            product.save(update_fields=['image'])
            print(f"[DEFAULT] Set: {product.name!r} -> product_images/{default_img}")
            updated += 1

print(f"\n--- Done: {updated} updated, {skipped} skipped ---")
