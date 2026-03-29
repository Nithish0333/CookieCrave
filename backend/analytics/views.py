from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime, timedelta
import json

from .models import UserBehavior, UserSession, UserJourney, HeatmapData
from .serializers import (
    UserBehaviorSerializer, UserSessionSerializer, 
    UserJourneySerializer, HeatmapDataSerializer, BulkBehaviorSerializer
)


class UserBehaviorViewSet(viewsets.ModelViewSet):
    serializer_class = UserBehaviorSerializer
    permission_classes = [AllowAny]  # Allow anonymous tracking
    
    def get_queryset(self):
        queryset = UserBehavior.objects.all()
        
        # Filter by user if authenticated
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        # Filter by action type
        action_type = self.request.query_params.get('action_type')
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        
        return queryset.order_by('-timestamp')
    
    @action(detail=False, methods=['post'])
    def bulk_track(self, request):
        """Track multiple behaviors at once"""
        serializer = BulkBehaviorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def analytics_summary(self, request):
        """Get analytics summary for dashboard"""
        queryset = self.get_queryset()
        
        # Basic metrics
        total_sessions = queryset.values('session_id').distinct().count()
        total_page_views = queryset.filter(action_type='page_view').count()
        total_product_views = queryset.filter(action_type='product_view').count()
        total_searches = queryset.filter(action_type='search').count()
        total_add_to_cart = queryset.filter(action_type='add_to_cart').count()
        total_purchases = queryset.filter(action_type='purchase').count()
        
        # Time metrics
        avg_session_duration = queryset.values('session_id').annotate(
            duration=Count('timestamp')
        ).aggregate(avg_duration=Avg('duration'))['avg_duration'] or 0
        
        # Popular pages
        popular_pages = queryset.filter(action_type='page_view').values(
            'page_url', 'page_title'
        ).annotate(count=Count('id')).order_by('-count')[:10]
        
        # Popular products
        popular_products = queryset.filter(action_type='product_view').values(
            'product__name', 'product__id'
        ).annotate(count=Count('id')).order_by('-count')[:10]
        
        # Recent search terms
        recent_searches = queryset.filter(action_type='search').values(
            'search_query'
        ).annotate(count=Count('id')).order_by('-count')[:10]
        
        return Response({
            'total_sessions': total_sessions,
            'total_page_views': total_page_views,
            'total_product_views': total_product_views,
            'total_searches': total_searches,
            'total_add_to_cart': total_add_to_cart,
            'total_purchases': total_purchases,
            'avg_session_duration': avg_session_duration,
            'popular_pages': list(popular_pages),
            'popular_products': list(popular_products),
            'recent_searches': list(recent_searches),
        })


class UserSessionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSessionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = UserSession.objects.all()
        
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset.order_by('-start_time')
    
    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """End a session and calculate duration"""
        session = self.get_object()
        session.end_time = timezone.now()
        
        if session.start_time:
            duration = (session.end_time - session.start_time).total_seconds()
            session.duration = int(duration)
        
        session.save()
        return Response(UserSessionSerializer(session).data)


class HeatmapDataViewSet(viewsets.ModelViewSet):
    serializer_class = HeatmapDataSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = HeatmapData.objects.all()
        
        # Filter by page URL
        page_url = self.request.query_params.get('page_url')
        if page_url:
            queryset = queryset.filter(page_url=page_url)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset.order_by('-timestamp')
    
    @action(detail=False, methods=['get'])
    def heatmap_data(self, request):
        """Get aggregated heatmap data for a page"""
        page_url = request.query_params.get('page_url')
        if not page_url:
            return Response({'error': 'page_url parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Get click data aggregated by position
        clicks = self.get_queryset().filter(page_url=page_url)
        
        # Create heatmap data grid
        heatmap_data = []
        for click in clicks:
            heatmap_data.append({
                'x': click.click_x,
                'y': click.click_y,
                'count': 1
            })
        
        return Response({
            'page_url': page_url,
            'clicks': heatmap_data,
            'total_clicks': clicks.count()
        })


@csrf_exempt
def track_event(request):
    """Simple endpoint for basic event tracking"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            metadata = data.get('metadata', {})
            
            # Handle product_id from metadata
            product = None
            if 'product_id' in metadata:
                product_id = metadata.pop('product_id')  # Remove from metadata
                try:
                    from products.models import Product
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    # If product doesn't exist, just keep the product_id in metadata
                    metadata['product_id'] = product_id
            
            # Create behavior record
            behavior = UserBehavior.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=data.get('session_id', ''),
                action_type=data.get('action_type', 'page_view'),
                page_url=data.get('page_url', ''),
                page_title=data.get('page_title', ''),
                product=product,
                search_query=data.get('search_query', ''),
                button_text=data.get('button_text', ''),
                time_on_page=data.get('time_on_page', 0),
                scroll_depth=data.get('scroll_depth', 0),
                metadata=metadata
            )
            
            return JsonResponse({'status': 'success', 'id': behavior.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST method allowed'}, status=405)
