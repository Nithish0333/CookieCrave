from django.contrib import admin
from .models import (
    UserPreference, UserRecommendation, RecommendationFeedback,
    TrendingItem, RecommendationHistory, RecommendationCache, UserBehavior
)


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'price_sensitivity', 'novelty_seeking', 'brand_loyalty', 'created_at']
    list_filter = ['price_sensitivity', 'novelty_seeking', 'brand_loyalty', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ['user', 'created_at', 'updated_at']
        }),
        ('Category Preferences', {
            'fields': ['category_preferences']
        }),
        ('Flavor Preferences', {
            'fields': ['favorite_flavors', 'disliked_flavors']
        }),
        ('Dietary Preferences', {
            'fields': ['dietary_restrictions', 'preferred_ingredients']
        }),
        ('Behavior Patterns', {
            'fields': ['price_sensitivity', 'novelty_seeking', 'brand_loyalty']
        }),
        ('Time Preferences', {
            'fields': ['preferred_order_times', 'seasonal_preferences']
        }),
    )


@admin.register(UserRecommendation)
class UserRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'algorithm', 'confidence_score', 'is_clicked', 'is_purchased', 'created_at']
    list_filter = ['algorithm', 'is_clicked', 'is_purchased', 'created_at']
    search_fields = ['user__username', 'product__name', 'algorithm']
    readonly_fields = ['created_at', 'clicked_at', 'purchased_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ['user', 'product', 'algorithm']
        }),
        ('Recommendation Details', {
            'fields': ['confidence_score', 'reason']
        }),
        ('Status', {
            'fields': ['is_active', 'is_clicked', 'is_purchased']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'clicked_at', 'purchased_at', 'expires_at']
        }),
    )


@admin.register(RecommendationFeedback)
class RecommendationFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommendation', 'feedback_type', 'rating', 'created_at']
    list_filter = ['feedback_type', 'rating', 'created_at']
    search_fields = ['user__username', 'feedback_type', 'comment']
    readonly_fields = ['created_at']


@admin.register(TrendingItem)
class TrendingItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'period', 'trending_score', 'velocity_score', 'view_count', 'purchase_count', 'period_start']
    list_filter = ['period', 'period_start']
    search_fields = ['product__name', 'category__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ['product', 'category', 'period']
        }),
        ('Metrics', {
            'fields': ['view_count', 'click_count', 'purchase_count', 'share_count']
        }),
        ('Scores', {
            'fields': ['trending_score', 'velocity_score']
        }),
        ('Time Period', {
            'fields': ['period_start', 'period_end']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at']
        }),
    )


@admin.register(RecommendationHistory)
class RecommendationHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'algorithm', 'created_at']
    list_filter = ['action_type', 'algorithm', 'created_at']
    search_fields = ['user__username', 'action_type', 'algorithm']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False  # History should be created automatically


@admin.register(RecommendationCache)
class RecommendationCacheAdmin(admin.ModelAdmin):
    list_display = ['user', 'algorithm', 'cache_key', 'hit_count', 'is_active', 'expires_at']
    list_filter = ['algorithm', 'is_active', 'created_at', 'expires_at']
    search_fields = ['user__username', 'algorithm', 'cache_key']
    readonly_fields = ['created_at', 'last_accessed', 'hit_count']
    
    def has_add_permission(self, request):
        return False  # Cache should be managed automatically


@admin.register(UserBehavior)
class UserBehaviorAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'behavior_type', 'quantity', 'value', 'created_at']
    list_filter = ['behavior_type', 'created_at', 'device_type']
    search_fields = ['user__username', 'product__name', 'behavior_type']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ['user', 'product', 'behavior_type']
        }),
        ('Behavior Details', {
            'fields': ['duration', 'quantity', 'value']
        }),
        ('Context', {
            'fields': ['session_id', 'device_type', 'referrer']
        }),
        ('Timestamp', {
            'fields': ['created_at']
        }),
    )
