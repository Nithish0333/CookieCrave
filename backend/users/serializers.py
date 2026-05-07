from rest_framework import serializers
from .models import User, SellerProfile

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['id', 'business_name', 'description', 'phone_number', 'address', 'phone_verified', 'created_at']
        read_only_fields = ['id', 'phone_verified', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    is_seller = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_seller']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        # Only check for duplicates if creating a new user
        if not self.instance and User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        # Only check for duplicates if creating a new user and email is provided
        if not self.instance and value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_password(self, value):
        # Simple password validation
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email', ''),
            username=validated_data['username'],
            cookie_balance=100
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_is_seller(self, obj):
        return hasattr(obj, 'seller_profile') and obj.seller_profile.phone_verified
