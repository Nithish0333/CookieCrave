from django.contrib import admin
from django.db.models import Count, Avg, Sum
from .models import UserBehavior, UserSession, UserJourney, HeatmapData


@admin.register(UserBehavior)
class UserBehaviorAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'session_id_short', 'action_type_display', 'page_title', 
        'product_name', 'product_category', 'timestamp', 'time_on_page'
    ]
    list_filter = [
        'action_type',
        'timestamp', 
        'user', 
        'product'
    ]
    search_fields = [
        'user__username', 'session_id', 'page_url', 'page_title',
        'search_query', 'button_text', 'product__name'
    ]
    readonly_fields = [
        'timestamp', 'ip_address', 'user_agent', 'referrer'
    ]
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    
    # Add fieldsets for better organization
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'session_id', 'action_type', 'timestamp')
        }),
        ('Page Information', {
            'fields': ('page_url', 'page_title', 'time_on_page', 'scroll_depth')
        }),
        ('Product Information', {
            'fields': ('product', 'search_query')
        }),
        ('Interaction Details', {
            'fields': ('button_text', 'element_selector')
        }),
        ('Technical Details', {
            'fields': ('ip_address', 'user_agent', 'referrer', 'metadata'),
            'classes': ('collapse',)
        }),
    )
    
    def session_id_short(self, obj):
        return obj.session_id[:8] + '...' if len(obj.session_id) > 8 else obj.session_id
    session_id_short.short_description = 'Session ID'
    
    def action_type_display(self, obj):
        # Get display value from choices
        for choice in obj.ACTION_TYPES:
            if choice[0] == obj.action_type:
                return choice[1]
        return obj.action_type.replace('_', ' ').title()
    action_type_display.short_description = 'Action Type'
    action_type_display.admin_order_field = 'action_type'
    
    def product_name(self, obj):
        if obj.product:
            return f"{obj.product.name} (ID: {obj.product.id})"
        return '-'
    product_name.short_description = 'Product'
    
    def product_category(self, obj):
        return obj.product.category.name if obj.product and obj.product.category else '-'
    product_category.short_description = 'Category'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product', 'product__category')
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            # Remove certain actions for non-superusers
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions
    
    # Add custom actions
    actions = ['mark_as_reviewed']
    
    def mark_as_reviewed(self, request, queryset):
        # This is just an example action - you can modify as needed
        count = queryset.count()
        self.message_user(request, f'{count} behaviors marked as reviewed.')
    mark_as_reviewed.short_description = "Mark selected behaviors as reviewed"


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'session_id_short', 'start_time', 'duration_formatted',
        'page_views', 'products_viewed', 'device_type'
    ]
    list_filter = [
        'start_time', 'device_type', 'browser', 'operating_system'
    ]
    search_fields = [
        'user__username', 'session_id', 'device_type', 'browser'
    ]
    readonly_fields = ['start_time']
    
    def session_id_short(self, obj):
        return obj.session_id[:8] + '...' if len(obj.session_id) > 8 else obj.session_id
    session_id_short.short_description = 'Session ID'
    
    def duration_formatted(self, obj):
        if obj.duration:
            hours = obj.duration // 3600
            minutes = (obj.duration % 3600) // 60
            seconds = obj.duration % 60
            if hours:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        return '-'
    duration_formatted.short_description = 'Duration'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(UserJourney)
class UserJourneyAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'session_short', 'start_time', 'goal_completed',
        'conversion_goal', 'steps_count'
    ]
    list_filter = [
        'goal_completed', 'start_time', 'conversion_goal'
    ]
    search_fields = [
        'user__username', 'entry_point', 'exit_point', 'conversion_goal'
    ]
    readonly_fields = ['start_time']
    
    def session_short(self, obj):
        return obj.session.session_id[:8] + '...' if obj.session else '-'
    session_short.short_description = 'Session'
    
    def steps_count(self, obj):
        return len(obj.steps) if obj.steps else 0
    steps_count.short_description = 'Steps'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'session')


@admin.register(HeatmapData)
class HeatmapDataAdmin(admin.ModelAdmin):
    list_display = [
        'page_url_short', 'click_position', 'viewport_size',
        'timestamp', 'user_or_session'
    ]
    list_filter = [
        'timestamp', 'page_url'
    ]
    search_fields = [
        'page_url', 'user__username', 'session_id'
    ]
    readonly_fields = ['timestamp']
    
    def page_url_short(self, obj):
        return obj.page_url[:50] + '...' if len(obj.page_url) > 50 else obj.page_url
    page_url_short.short_description = 'Page URL'
    
    def click_position(self, obj):
        return f"({obj.click_x}, {obj.click_y})"
    click_position.short_description = 'Click Position'
    
    def viewport_size(self, obj):
        return f"{obj.viewport_width}x{obj.viewport_height}"
    viewport_size.short_description = 'Viewport'
    
    def user_or_session(self, obj):
        if obj.user:
            return obj.user.username
        return obj.session_id[:8] + '...' if obj.session_id else '-'
    user_or_session.short_description = 'User/Session'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


# Custom admin site with analytics dashboard
class AnalyticsAdminSite(admin.AdminSite):
    site_header = "Cookie Analytics"
    site_title = "Cookie Analytics Portal"
    index_title = "Welcome to Cookie Analytics Portal"
    
    def get_urls(self):
        from django.urls import path
        from django.shortcuts import render
        from django.http import JsonResponse
        from django.db.models import Count, Avg, Sum
        from datetime import datetime, timedelta
        
        urls = super().get_urls()
        
        def analytics_dashboard(request):
            # Get analytics data
            last_30_days = datetime.now() - timedelta(days=30)
            
            # Basic metrics
            total_sessions = UserSession.objects.filter(
                start_time__gte=last_30_days
            ).count()
            
            total_page_views = UserBehavior.objects.filter(
                timestamp__gte=last_30_days,
                action_type='page_view'
            ).count()
            
            total_product_views = UserBehavior.objects.filter(
                timestamp__gte=last_30_days,
                action_type='product_view'
            ).count()
            
            total_purchases = UserBehavior.objects.filter(
                timestamp__gte=last_30_days,
                action_type='purchase'
            ).count()
            
            # Popular pages
            popular_pages = UserBehavior.objects.filter(
                timestamp__gte=last_30_days,
                action_type='page_view'
            ).values('page_url', 'page_title').annotate(
                count=Count('id')
            ).order_by('-count')[:10]
            
            # Popular products
            popular_products = UserBehavior.objects.filter(
                timestamp__gte=last_30_days,
                action_type='product_view'
            ).values('product__name').annotate(
                count=Count('id')
            ).order_by('-count')[:10]
            
            context = {
                'total_sessions': total_sessions,
                'total_page_views': total_page_views,
                'total_product_views': total_product_views,
                'total_purchases': total_purchases,
                'popular_pages': popular_pages,
                'popular_products': popular_products,
            }
            
            return render(request, 'admin/analytics_dashboard.html', context)
        
        custom_urls = [
            path('analytics-dashboard/', analytics_dashboard, name='analytics_dashboard'),
        ]
        return custom_urls + urls


# Create custom admin site
analytics_admin = AnalyticsAdminSite(name='analytics_admin')

# Register models with custom admin site
analytics_admin.register(UserBehavior, UserBehaviorAdmin)
analytics_admin.register(UserSession, UserSessionAdmin)
analytics_admin.register(UserJourney, UserJourneyAdmin)
analytics_admin.register(HeatmapData, HeatmapDataAdmin)
