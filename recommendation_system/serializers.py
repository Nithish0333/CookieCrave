from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    UserPreference, UserRecommendation, RecommendationFeedback,
    TrendingItem, RecommendationHistory, RecommendationCache, UserBehavior
)
from products.models import Product, Category
from products.serializers import ProductSerializer, CategorySerializer

User = get_user_model()


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = [
            'id', 'user', 'category_preferences', 'favorite_flavors',
            'disliked_flavors', 'dietary_restrictions', 'preferred_ingredients',
            'price_sensitivity', 'novelty_seeking', 'brand_loyalty',
            'preferred_order_times', 'seasonal_preferences',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def update(self, instance, validated_data):
        # Merge JSON fields instead of replacing
        for field in ['category_preferences', 'seasonal_preferences']:
            if field in validated_data:
                current_data = getattr(instance, field) or {}
                new_data = validated_data[field]
                current_data.update(new_data)
                validated_data[field] = current_data
        
        for field in ['favorite_flavors', 'disliked_flavors', 'dietary_restrictions', 
                     'preferred_ingredients', 'preferred_order_times']:
            if field in validated_data:
                current_data = getattr(instance, field) or []
                new_data = validated_data[field]
                # Combine lists without duplicates
                combined = list(set(current_data + new_data))
                validated_data[field] = combined
        
        return super().update(instance, validated_data)


class UserRecommendationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserRecommendation
        fields = [
            'id', 'user', 'product', 'product_id', 'algorithm',
            'confidence_score', 'reason', 'is_active', 'is_clicked',
            'is_purchased', 'created_at', 'clicked_at', 'purchased_at', 'expires_at'
        ]
        read_only_fields = ['user', 'created_at', 'clicked_at', 'purchased_at']


class RecommendationFeedbackSerializer(serializers.ModelSerializer):
    recommendation = UserRecommendationSerializer(read_only=True)
    recommendation_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = RecommendationFeedback
        fields = [
            'id', 'recommendation', 'recommendation_id', 'user',
            'feedback_type', 'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']


class TrendingItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = TrendingItem
        fields = [
            'id', 'product', 'category', 'view_count', 'click_count',
            'purchase_count', 'share_count', 'trending_score', 'velocity_score',
            'period', 'period_start', 'period_end', 'created_at', 'updated_at'
        ]


class RecommendationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationHistory
        fields = [
            'id', 'user', 'action_type', 'product_ids', 'algorithm',
            'context', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']


class RecommendationCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationCache
        fields = [
            'id', 'user', 'cache_key', 'algorithm', 'product_data',
            'hit_count', 'is_active', 'created_at', 'last_accessed', 'expires_at'
        ]
        read_only_fields = ['user', 'created_at', 'last_accessed', 'hit_count']


class UserBehaviorSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserBehavior
        fields = [
            'id', 'user', 'product', 'product_id', 'behavior_type',
            'duration', 'quantity', 'value', 'session_id',
            'device_type', 'referrer', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']


class RecommendationRequestSerializer(serializers.Serializer):
    """Serializer for recommendation request parameters"""
    algorithm = serializers.ChoiceField(
        choices=['personalized', 'collaborative', 'content_based', 
                'popularity', 'seasonal', 'trending', 'hybrid'],
        default='hybrid'
    )
    limit = serializers.IntegerField(default=20, min_value=1, max_value=100)
    exclude_purchased = serializers.BooleanField(default=True)
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="Filter by specific categories"
    )
    price_range = serializers.DictField(
        required=False,
        help_text="{'min': price, 'max': price}"
    )


class RecommendationResponseSerializer(serializers.Serializer):
    """Serializer for recommendation response"""
    recommendations = ProductSerializer(many=True)
    algorithm = serializers.CharField()
    total_count = serializers.IntegerField()
    confidence_scores = serializers.DictField(
        child=serializers.FloatField(),
        required=False
    )
    reasons = serializers.DictField(
        child=serializers.CharField(),
        required=False
    )


class FeedbackRequestSerializer(serializers.Serializer):
    """Serializer for feedback submission"""
    recommendation_id = serializers.IntegerField()
    feedback_type = serializers.ChoiceField(
        choices=['like', 'dislike', 'not_interested', 'already_purchased', 'not_relevant']
    )
    rating = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=5
    )
    comment = serializers.CharField(required=False, allow_blank=True)


class PreferenceUpdateSerializer(serializers.Serializer):
    """Serializer for updating user preferences"""
    category_preferences = serializers.DictField(
        child=serializers.FloatField(min_value=0, max_value=1),
        required=False
    )
    favorite_flavors = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    disliked_flavors = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    dietary_restrictions = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    preferred_ingredients = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    price_sensitivity = serializers.FloatField(
        min_value=0, max_value=1, required=False
    )
    novelty_seeking = serializers.FloatField(
        min_value=0, max_value=1, required=False
    )
    brand_loyalty = serializers.FloatField(
        min_value=0, max_value=1, required=False
    )
    seasonal_preferences = serializers.DictField(
        required=False
    )


class TrendingRequestSerializer(serializers.Serializer):
    """Serializer for trending items request"""
    period = serializers.ChoiceField(
        choices=['hourly', 'daily', 'weekly', 'monthly'],
        default='daily'
    )
    category_id = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(default=20, min_value=1, max_value=100)


class RecommendationStatsSerializer(serializers.Serializer):
    """Serializer for recommendation statistics"""
    total_recommendations = serializers.IntegerField()
    click_rate = serializers.FloatField()
    purchase_rate = serializers.FloatField()
    feedback_rate = serializers.FloatField()
    algorithm_performance = serializers.DictField()
    category_performance = serializers.DictField()
    time_period = serializers.CharField()
