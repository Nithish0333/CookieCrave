from django.db import models
from django.conf import settings
from products.models import Product
import json


class UserBehavior(models.Model):
    """Main tracking model for user behavior"""
    
    ACTION_TYPES = [
        ('page_view', 'Page View'),
        ('home_page_view', 'Home Page View'),
        ('about_page_view', 'About Page View'),
        ('contact_page_view', 'Contact Page View'),
        ('selling_page_view', 'Selling Page View'),
        ('purchase_page_view', 'Purchase Page View'),
        ('product_view', 'Product View'),
        ('button_click', 'Button Click'),
        ('search', 'Search'),
        ('add_to_cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
        ('scroll', 'Scroll Behavior'),
        ('session_start', 'Session Start'),
        ('session_end', 'Session End'),
        ('user_identified', 'User Identified'),
        ('page_leave', 'Page Leave'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=255, db_index=True)  # For anonymous users
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    page_url = models.URLField(max_length=500, blank=True)
    page_title = models.CharField(max_length=255, blank=True)
    
    # Product related tracking
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Search and interaction data
    search_query = models.CharField(max_length=255, blank=True)
    button_text = models.CharField(max_length=255, blank=True)
    element_selector = models.CharField(max_length=500, blank=True)
    
    # Time tracking
    timestamp = models.DateTimeField(auto_now_add=True)
    time_on_page = models.PositiveIntegerField(default=0)  # in seconds
    scroll_depth = models.IntegerField(default=0)  # percentage
    
    # Additional metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(max_length=500, blank=True)
    
    # Extra data as JSON
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['session_id', 'timestamp']),
            models.Index(fields=['action_type', 'timestamp']),
            models.Index(fields=['product', 'timestamp']),
        ]
    
    def __str__(self):
        user_info = self.user.username if self.user else f"Session:{self.session_id[:8]}"
        return f"{user_info} - {self.action_type} at {self.timestamp}"


class UserSession(models.Model):
    """Track user sessions for time analysis"""
    
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)  # in seconds
    page_views = models.PositiveIntegerField(default=0)
    products_viewed = models.PositiveIntegerField(default=0)
    searches_made = models.PositiveIntegerField(default=0)
    items_added_to_cart = models.PositiveIntegerField(default=0)
    purchases_made = models.PositiveIntegerField(default=0)
    total_scroll_depth = models.IntegerField(default=0)
    
    # Device and browser info
    device_type = models.CharField(max_length=50, blank=True)  # mobile, desktop, tablet
    browser = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    screen_resolution = models.CharField(max_length=20, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'start_time']),
            models.Index(fields=['session_id']),
        ]
    
    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"Session {self.session_id[:8]} - {user_info} ({self.duration}s)"


class UserJourney(models.Model):
    """Track complete user journeys through the application"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Journey metadata
    entry_point = models.URLField(max_length=500)  # First page visited
    exit_point = models.URLField(max_length=500, blank=True)  # Last page visited
    conversion_goal = models.CharField(max_length=100, blank=True)  # What action we wanted
    goal_completed = models.BooleanField(default=False)
    
    # Journey steps as JSON array
    steps = models.JSONField(default=list)  # Array of action sequences
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'start_time']),
            models.Index(fields=['session', 'start_time']),
            models.Index(fields=['goal_completed']),
        ]
    
    def __str__(self):
        return f"Journey for {self.user.username} - {'Completed' if self.goal_completed else 'In Progress'}"


class HeatmapData(models.Model):
    """Store click and scroll data for heatmap visualization"""
    
    page_url = models.URLField(max_length=500)
    click_x = models.IntegerField()
    click_y = models.IntegerField()
    viewport_width = models.IntegerField()
    viewport_height = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=255, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['page_url', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]
    
    def __str__(self):
        return f"Click at ({self.click_x}, {self.click_y}) on {self.page_url}"
