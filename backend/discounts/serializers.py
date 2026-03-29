from rest_framework import serializers
from .models import UserDiscount

class UserDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDiscount
        fields = ['id', 'code', 'discount_percentage', 'game_type', 'is_used', 'created_at', 'expires_at']
        read_only_fields = ['id', 'code', 'created_at', 'expires_at', 'is_used']
