#!/usr/bin/env python
"""Check the actual API response structure to debug image field."""

import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product
from products.serializers import ProductSerializer
from django.http import JsonResponse
from rest_framework.serializers import ModelSerializer

# Test the serializer response
product = Product.objects.first()

if product:
    serializer = ProductSerializer(product)
    data = serializer.data
    
    print(json.dumps(data, indent=2, default=str))
else:
    print("No products found")
