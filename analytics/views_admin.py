from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
from .models import UserBehavior, UserSession, UserJourney, HeatmapData


def analytics_dashboard_view(request):
    """Analytics dashboard view for admin"""
    # Get data from last 30 days
    last_30_days = timezone.now() - timedelta(days=30)
    
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
    
    total_searches = UserBehavior.objects.filter(
        timestamp__gte=last_30_days,
        action_type='search'
    ).count()
    
    total_add_to_cart = UserBehavior.objects.filter(
        timestamp__gte=last_30_days,
        action_type='add_to_cart'
    ).count()
    
    total_purchases = UserBehavior.objects.filter(
        timestamp__gte=last_30_days,
        action_type='purchase'
    ).count()
    
    # Average session duration
    avg_session_duration = UserSession.objects.filter(
        start_time__gte=last_30_days
    ).aggregate(avg_duration=Avg('duration'))['avg_duration'] or 0
    
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
    
    # Recent search terms
    recent_searches = UserBehavior.objects.filter(
        timestamp__gte=last_30_days,
        action_type='search'
    ).values('search_query').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    context = {
        'total_sessions': total_sessions,
        'total_page_views': total_page_views,
        'total_product_views': total_product_views,
        'total_searches': total_searches,
        'total_add_to_cart': total_add_to_cart,
        'total_purchases': total_purchases,
        'avg_session_duration': avg_session_duration,
        'popular_pages': popular_pages,
        'popular_products': popular_products,
        'recent_searches': recent_searches,
    }
    
    return render(request, 'admin/analytics_dashboard.html', context)
