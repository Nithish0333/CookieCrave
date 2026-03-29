from rest_framework import serializers
from .models import Payment, Order, OrderItem
from products.serializers import ProductSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'razorpay_order_id', 'razorpay_payment_id', 'amount', 
                 'currency', 'status', 'created_at', 'updated_at']
        read_only_fields = ['razorpay_order_id', 'razorpay_payment_id', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'status', 'shipping_address', 'phone_number',
                 'items', 'payment', 'created_at', 'updated_at']
        read_only_fields = ['order_id', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )
    shipping_address = serializers.CharField(max_length=500)
    phone_number = serializers.CharField(max_length=15)
    
    def validate_items(self, items):
        product_ids = [item.get('product_id') for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Duplicate products in order")
        return items
