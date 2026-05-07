from rest_framework import serializers
from .models import Product, Category, Wishlist, Rating
import base64

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_image(self, obj):
        """Get category image URL."""
        if obj.image_url:
            return obj.image_url
        return "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80"

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'category_id', 'seller', 'seller_username', 'image', 'stock', 'created_at']
        read_only_fields = ('seller', 'created_at')
    
    def get_image(self, obj):
        """Serve image from PostgreSQL database as base64 or return URL."""
        if obj.image_data:
            # Convert binary data to base64 for frontend
            image_base64 = base64.b64encode(obj.image_data).decode('utf-8')
            return f"data:image/jpeg;base64,{image_base64}"
        elif obj.image_url:
            return obj.image_url
        else:
            # Fallback to a default image
            return "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&q=80"

class RatingSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Rating
        fields = ['id', 'user', 'user_username', 'product', 'product_name', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ('user', 'created_at', 'updated_at')


class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'user_username', 'products', 'product_ids', 'created_at', 'updated_at']
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        product_ids = validated_data.pop('product_ids', [])
        wishlist = Wishlist.objects.create(**validated_data)
        if product_ids:
            wishlist.products.set(product_ids)
        return wishlist

    def update(self, instance, validated_data):
        product_ids = validated_data.pop('product_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if product_ids is not None:
            instance.products.set(product_ids)
        
        return instance

