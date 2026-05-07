from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from products.models import Product, Category
import json

User = get_user_model()


class UserPreference(models.Model):
    """Store user preferences and behavior patterns"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    
    # Category preferences with weights
    category_preferences = models.JSONField(default=dict, help_text="Category ID -> preference weight (0-1)")
    
    # Flavor preferences
    favorite_flavors = models.JSONField(default=list, help_text="List of favorite flavor tags")
    disliked_flavors = models.JSONField(default=list, help_text="List of disliked flavor tags")
    
    # Dietary preferences
    dietary_restrictions = models.JSONField(default=list, help_text="List of dietary restrictions")
    preferred_ingredients = models.JSONField(default=list, help_text="List of preferred ingredients")
    
    # Behavior patterns
    price_sensitivity = models.FloatField(default=0.5, help_text="0=price insensitive, 1=very price sensitive")
    novelty_seeking = models.FloatField(default=0.5, help_text="0=conservative, 1=loves new things")
    brand_loyalty = models.FloatField(default=0.5, help_text="0=not loyal, 1=very loyal")
    
    # Time-based preferences
    preferred_order_times = models.JSONField(default=list, help_text="Preferred hours for ordering")
    seasonal_preferences = models.JSONField(default=dict, help_text="Season -> category preferences")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s preferences"


class UserRecommendation(models.Model):
    """Store personalized recommendations with confidence scores"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='recommendations')
    
    # Recommendation details
    algorithm = models.CharField(max_length=50, help_text="Algorithm that generated this recommendation")
    confidence_score = models.FloatField(help_text="Confidence score (0-1)")
    reason = models.TextField(blank=True, help_text="Why this was recommended")
    
    # Recommendation metadata
    is_active = models.BooleanField(default=True)
    is_clicked = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    purchased_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['algorithm', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.product.name} for {self.user.username}"


class RecommendationFeedback(models.Model):
    """Track user feedback on recommendations"""
    recommendation = models.OneToOneField(UserRecommendation, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Feedback types
    FEEDBACK_TYPES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('not_interested', 'Not Interested'),
        ('already_purchased', 'Already Purchased'),
        ('not_relevant', 'Not Relevant'),
    ]
    
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    rating = models.IntegerField(null=True, blank=True, help_text="1-5 rating if applicable")
    comment = models.TextField(blank=True)
    
    # Feedback metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'feedback_type']),
            models.Index(fields=['feedback_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.feedback_type}"


class TrendingItem(models.Model):
    """Track trending products and categories"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='trending_data')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    # Trending metrics
    view_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    purchase_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    
    # Trending scores
    trending_score = models.FloatField(default=0, help_text="Overall trending score")
    velocity_score = models.FloatField(default=0, help_text="Rate of increase")
    
    # Time periods
    PERIOD_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='daily')
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['period', 'period_start']),
            models.Index(fields=['trending_score']),
            models.Index(fields=['velocity_score']),
        ]
        unique_together = ['product', 'period', 'period_start']
    
    def __str__(self):
        return f"{self.product.name} - {self.period} trending"


class RecommendationHistory(models.Model):
    """Track user's recommendation history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_history')
    
    # History details
    action_type = models.CharField(max_length=20, help_text="viewed, clicked, purchased, feedback")
    product_ids = models.JSONField(help_text="List of product IDs involved")
    algorithm = models.CharField(max_length=50, blank=True)
    
    # Context data
    context = models.JSONField(default=dict, help_text="Additional context like time, device, etc.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.action_type}"


class RecommendationCache(models.Model):
    """Cache for pre-computed recommendations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cached_recommendations')
    
    # Cache key and data
    cache_key = models.CharField(max_length=255, help_text="Unique cache key")
    algorithm = models.CharField(max_length=50)
    product_data = models.JSONField(help_text="Cached product recommendations")
    
    # Cache metadata
    hit_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'algorithm']),
            models.Index(fields=['cache_key']),
            models.Index(fields=['expires_at']),
        ]
        unique_together = ['user', 'cache_key']
    
    def __str__(self):
        return f"Cache for {self.user.username} - {self.algorithm}"


class UserBehavior(models.Model):
    """Track detailed user behavior for better recommendations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behaviors')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='user_behaviors')
    
    # Behavior types
    BEHAVIOR_TYPES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('add_to_cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
        ('review', 'Review'),
        ('share', 'Share'),
        ('wishlist', 'Add to Wishlist'),
    ]
    
    behavior_type = models.CharField(max_length=20, choices=BEHAVIOR_TYPES)
    
    # Behavior details
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in seconds for views")
    quantity = models.PositiveIntegerField(default=1)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Context
    session_id = models.CharField(max_length=255, blank=True)
    device_type = models.CharField(max_length=50, blank=True)
    referrer = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'behavior_type', 'created_at']),
            models.Index(fields=['product', 'behavior_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.behavior_type} - {self.product.name}"
