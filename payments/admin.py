from django.contrib import admin
from .models import Payment, Order, OrderItem


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['razorpay_order_id', 'razorpay_payment_id', 'amount', 'currency', 'status', 'user', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['razorpay_order_id', 'razorpay_payment_id', 'user__username']
    readonly_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'payment', 'status', 'shipping_address', 'phone_number', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_id', 'payment__razorpay_order_id', 'shipping_address']
    readonly_fields = ['order_id', 'created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order__created_at']
    search_fields = ['order__order_id', 'product__name']
