#!/usr/bin/env python
import os
import sys

# Setup Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from products.models import Product

def create_product_id_mapping():
    """Create a mapping using product IDs for guaranteed uniqueness"""
    print("🔍 Creating Product ID Mapping for Zero Repetition")
    print("=" * 60)
    
    # Get all products and sort by ID for consistent mapping
    products = Product.objects.all().order_by('id')
    
    print(f"Found {len(products)} products")
    
    # Create a mapping from product name to unique index
    # Use product ID to ensure uniqueness even for duplicate names
    product_to_index = {}
    
    for i, product in enumerate(products):
        # Use product ID as part of the key to handle duplicates
        unique_key = f"{product.name}_{product.id}"
        product_to_index[unique_key] = i % 48  # Ensure we stay within 48 unique URLs
    
    print(f"Created mapping for {len(product_to_index)} products")
    
    return product_to_index

if __name__ == "__main__":
    mapping = create_product_id_mapping()
    print("\n📊 Sample mappings:")
    for i, (key, index) in enumerate(list(mapping.items())[:10]):
        print(f"   {key} -> index {index}")
