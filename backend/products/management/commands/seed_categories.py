from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Seed categories: Chocolate Chip, Cakes, Milkshakes, Chocolates, Fruit and Nuts, Oatmeal'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Chocolate Chip', 'description': 'Classic chocolate chip cookies',
             'image_url': 'https://images.unsplash.com/photo-1511381939415-e44015466834?w=400&h=200&fit=crop'},
            {'name': 'Cakes', 'description': 'Delicious cakes and cake slices',
             'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=200&fit=crop'},
            {'name': 'Milkshakes', 'description': 'Creamy milkshakes and cold drinks',
             'image_url': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=200&fit=crop'},
            {'name': 'Chocolates', 'description': 'Rich chocolates and truffles',
             'image_url': 'https://images.unsplash.com/photo-1511381939415-e44015466834?w=400&h=200&fit=crop'},
            {'name': 'Fruit and Nuts', 'description': 'Cookies with dried fruits and crunchy nuts',
             'image_url': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400&h=200&fit=crop'},
            {'name': 'Oatmeal', 'description': 'Hearty oatmeal and raisin cookies',
             'image_url': 'https://images.unsplash.com/photo-1623334044303-2412a4c5afd5?w=400&h=200&fit=crop'},
        ]

        names = [c['name'] for c in categories]
        deleted, _ = Category.objects.exclude(name__in=names).delete()
        if deleted:
            self.stdout.write(self.style.WARNING(f"Removed {deleted} old categories."))

        created = 0
        for cat in categories:
            obj, was_created = Category.objects.update_or_create(
                name=cat['name'],
                defaults={'description': cat['description'], 'image_url': cat.get('image_url', '')}
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created category: {obj.name}"))
            else:
                self.stdout.write(f"Updated category: {obj.name}")

        self.stdout.write(self.style.SUCCESS(f'\nDone! Categories: All Cookies, Chocolate Chip, Cakes, Milkshakes, Chocolates, Fruit and Nuts, Oatmeal'))
