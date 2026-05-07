from django.core.management.base import BaseCommand
from products.models import Product, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed sample products for each category'

    def handle(self, *args, **kwargs):
        # Get or create a default seller
        seller, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@cookiecrave.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            seller.set_password('admin123')
            seller.save()
            self.stdout.write(self.style.SUCCESS(f"Created admin user"))
        
        products_data = [
            # Chocolate Chip
            {
                'name': 'Classic Chocolate Chip Cookies',
                'description': 'Traditional chocolate chip cookies with premium chocolate',
                'price': 150,
                'stock': 50,
                'category': 'Chocolate Chip',
                'image': 'product_images/chocolate_chip_cookies.jpg'
            },
            {
                'name': 'Double Chocolate Chip',
                'description': 'Extra chocolatey with double chocolate chips',
                'price': 180,
                'stock': 40,
                'category': 'Chocolate Chip',
                'image': 'product_images/double_chocolate_chip.jpg'
            },
            {
                'name': 'White Chocolate Chip',
                'description': 'Buttery cookies with white chocolate chips',
                'price': 160,
                'stock': 35,
                'category': 'Chocolate Chip',
                'image': 'product_images/white_chocolate_chip.jpg'
            },
            
            # Cakes
            {
                'name': 'Chocolate Cake Slice',
                'description': 'Rich and moist chocolate cake',
                'price': 250,
                'stock': 30,
                'category': 'Cakes',
                'image': 'product_images/chocolate_cake.jpg'
            },
            {
                'name': 'Vanilla Cake',
                'description': 'Classic vanilla cake with vanilla frosting',
                'price': 220,
                'stock': 25,
                'category': 'Cakes',
                'image': 'product_images/vanilla_cake.jpg'
            },
            {
                'name': 'Strawberry Cake',
                'description': 'Fresh strawberry cake with cream',
                'price': 280,
                'stock': 20,
                'category': 'Cakes',
                'image': 'product_images/strawberry_cake.jpg'
            },
            
            # Milkshakes
            {
                'name': 'Chocolate Milkshake',
                'description': 'Creamy chocolate milkshake',
                'price': 120,
                'stock': 60,
                'category': 'Milkshakes',
                'image': 'product_images/chocolate_milkshake.jpg'
            },
            {
                'name': 'Vanilla Milkshake',
                'description': 'Classic vanilla milkshake',
                'price': 100,
                'stock': 55,
                'category': 'Milkshakes',
                'image': 'product_images/vanilla_milkshake.jpg'
            },
            {
                'name': 'Strawberry Milkshake',
                'description': 'Fresh strawberry milkshake',
                'price': 130,
                'stock': 50,
                'category': 'Milkshakes',
                'image': 'product_images/strawberry_milkshake.jpg'
            },
            
            # Chocolates
            {
                'name': 'Dark Chocolate Bar',
                'description': '70% dark chocolate bar',
                'price': 200,
                'stock': 45,
                'category': 'Chocolates',
                'image': 'product_images/dark_chocolate.jpg'
            },
            {
                'name': 'Milk Chocolate Bar',
                'description': 'Smooth milk chocolate bar',
                'price': 180,
                'stock': 50,
                'category': 'Chocolates',
                'image': 'product_images/milk_chocolate.jpg'
            },
            {
                'name': 'Chocolate Truffles',
                'description': 'Assorted chocolate truffles (6 pieces)',
                'price': 300,
                'stock': 30,
                'category': 'Chocolates',
                'image': 'product_images/chocolate_truffles.jpg'
            },
            
            # Fruit and Nuts
            {
                'name': 'Almond Cookies',
                'description': 'Crunchy almond cookies',
                'price': 170,
                'stock': 40,
                'category': 'Fruit and Nuts',
                'image': 'product_images/almond_cookies.jpg'
            },
            {
                'name': 'Cranberry Cookies',
                'description': 'Tart cranberry cookies',
                'price': 160,
                'stock': 35,
                'category': 'Fruit and Nuts',
                'image': 'product_images/cranberry_cookies.jpg'
            },
            {
                'name': 'Walnut Cookies',
                'description': 'Nutty walnut cookies',
                'price': 175,
                'stock': 38,
                'category': 'Fruit and Nuts',
                'image': 'product_images/walnut_cookies.jpg'
            },
            
            # Oatmeal
            {
                'name': 'Oatmeal Raisin Cookies',
                'description': 'Hearty oatmeal with raisins',
                'price': 140,
                'stock': 55,
                'category': 'Oatmeal',
                'image': 'product_images/oatmeal_raisin.jpg'
            },
            {
                'name': 'Oatmeal Honey Cookies',
                'description': 'Sweet oatmeal with honey',
                'price': 150,
                'stock': 50,
                'category': 'Oatmeal',
                'image': 'product_images/oatmeal_honey.jpg'
            },
            {
                'name': 'Oatmeal Cranberry Cookies',
                'description': 'Oatmeal with tart cranberries',
                'price': 160,
                'stock': 45,
                'category': 'Oatmeal',
                'image': 'product_images/oatmeal_cranberry.jpg'
            },
        ]

        created_count = 0
        for product_data in products_data:
            category = Category.objects.get(name=product_data['category'])
            product, was_created = Product.objects.update_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'category': category,
                    'seller': seller,
                    'image': product_data['image']
                }
            )
            if was_created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))
            else:
                self.stdout.write(f"Updated product: {product.name}")

        self.stdout.write(self.style.SUCCESS(f'\nDone! Created {created_count} new products.'))
