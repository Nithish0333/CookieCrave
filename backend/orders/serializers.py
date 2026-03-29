from rest_framework import serializers
from .models import Transaction, Order
from products.serializers import ProductSerializer


class TransactionSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('user', 'total_price', 'status')


class OrderSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
