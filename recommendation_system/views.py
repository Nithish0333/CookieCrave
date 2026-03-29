from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count, Q, Avg, F
from datetime import timedelta
from collections import defaultdict

from .models import (
    UserPreference, UserRecommendation, RecommendationFeedback,
    TrendingItem, RecommendationHistory, UserBehavior
)
from .serializers import (
    UserPreferenceSerializer, UserRecommendationSerializer,
    RecommendationFeedbackSerializer, TrendingItemSerializer,
    RecommendationHistorySerializer, UserBehaviorSerializer,
    RecommendationRequestSerializer, RecommendationResponseSerializer,
    FeedbackRequestSerializer, PreferenceUpdateSerializer,
    TrendingRequestSerializer, RecommendationStatsSerializer
)
from .recommendations import RecommendationEngine
from products.models import Product, Category

User = get_user_model()


class RecommendationAPIView(APIView):
    """Main recommendation API endpoint"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get recommendations for the current user"""
        serializer = RecommendationRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            algorithm = serializer.validated_data.get('algorithm', 'hybrid')
            limit = serializer.validated_data.get('limit', 20)
            exclude_purchased = serializer.validated_data.get('exclude_purchased', True)
            category_ids = serializer.validated_data.get('category_ids')
            price_range = serializer.validated_data.get('price_range')
            
            # Get recommendations
            engine = RecommendationEngine(request.user)
            recommendations = engine.get_recommendations(
                algorithm=algorithm,
                limit=limit,
                exclude_purchased=exclude_purchased
            )
            
            # Apply additional filters
            if category_ids:
                recommendations = recommendations.filter(category_id__in=category_ids)
            
            if price_range:
                min_price = price_range.get('min')
                max_price = price_range.get('max')
                if min_price is not None:
                    recommendations = recommendations.filter(price__gte=min_price)
                if max_price is not None:
                    recommendations = recommendations.filter(price__lte=max_price)
            
            # Store recommendations in database
            stored_recommendations = []
            for product in recommendations:
                rec, created = UserRecommendation.objects.get_or_create(
                    user=request.user,
                    product=product,
                    algorithm=algorithm,
                    defaults={
                        'confidence_score': 0.8,  # Default confidence
                        'reason': f'Recommended by {algorithm} algorithm',
                        'expires_at': timezone.now() + timedelta(days=7)
                    }
                )
                if not created:
                    rec.is_active = True
                    rec.save()
                stored_recommendations.append(rec)
            
            # Track recommendation history
            RecommendationHistory.objects.create(
                user=request.user,
                action_type='viewed',
                product_ids=[p.id for p in recommendations],
                algorithm=algorithm,
                context={'limit': limit, 'filters': request.query_params.dict()}
            )
            
            # Prepare response
            from products.serializers import ProductSerializer
            product_serializer = ProductSerializer(recommendations, many=True)
            
            response_data = {
                'recommendations': product_serializer.data,
                'algorithm': algorithm,
                'total_count': len(recommendations),
                'confidence_scores': {str(rec.product.id): rec.confidence_score for rec in stored_recommendations},
                'reasons': {str(rec.product.id): rec.reason for rec in stored_recommendations}
            }
            # Return raw serialized data to avoid nested serializer issues
            return Response(response_data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        """Create a specific recommendation"""
        product_id = request.data.get('product_id')
        algorithm = request.data.get('algorithm', 'manual')
        confidence_score = request.data.get('confidence_score', 0.5)
        reason = request.data.get('reason', 'Manual recommendation')
        
        try:
            product = Product.objects.get(id=product_id, stock__gt=0)
            
            recommendation = UserRecommendation.objects.create(
                user=request.user,
                product=product,
                algorithm=algorithm,
                confidence_score=confidence_score,
                reason=reason,
                expires_at=timezone.now() + timedelta(days=7)
            )
            
            serializer = UserRecommendationSerializer(recommendation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found or out of stock'},
                status=status.HTTP_404_NOT_FOUND
            )


class RecommendationFeedbackAPIView(APIView):
    """Handle feedback on recommendations"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Submit feedback on a recommendation"""
        serializer = FeedbackRequestSerializer(data=request.data)
        if serializer.is_valid():
            recommendation_id = serializer.validated_data['recommendation_id']
            feedback_type = serializer.validated_data['feedback_type']
            rating = serializer.validated_data.get('rating')
            comment = serializer.validated_data.get('comment', '')
            
            engine = RecommendationEngine(request.user)
            feedback = engine.record_feedback(
                recommendation_id, feedback_type, rating, comment
            )
            
            if feedback:
                # Update recommendation status
                try:
                    recommendation = feedback.recommendation
                    if feedback_type == 'like':
                        recommendation.is_clicked = True
                    elif feedback_type == 'already_purchased':
                        recommendation.is_purchased = True
                    
                    recommendation.save()
                except:
                    pass
                
                # Track feedback history
                RecommendationHistory.objects.create(
                    user=request.user,
                    action_type='feedback',
                    product_ids=[recommendation.product.id],
                    algorithm=recommendation.algorithm,
                    context={'feedback_type': feedback_type, 'rating': rating}
                )
                
                return Response(
                    RecommendationFeedbackSerializer(feedback).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': 'Recommendation not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPreferenceAPIView(APIView):
    """Manage user preferences"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user preferences"""
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(preferences)
        return Response(serializer.data)
    
    def put(self, request):
        """Update user preferences"""
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        
        serializer = PreferenceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            # Update preferences with validated data
            for field, value in serializer.validated_data.items():
                setattr(preferences, field, value)
            
            preferences.save()
            
            # Clear recommendation cache when preferences change
            RecommendationCache.objects.filter(
                user=request.user,
                is_active=True
            ).update(is_active=False)
            
            return Response(UserPreferenceSerializer(preferences).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrendingItemsAPIView(APIView):
    """Get trending items"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get trending products"""
        serializer = TrendingRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            period = serializer.validated_data.get('period', 'daily')
            category_id = serializer.validated_data.get('category_id')
            limit = serializer.validated_data.get('limit', 20)
            
            # Calculate time range
            if period == 'hourly':
                start_time = timezone.now() - timedelta(hours=24)
            elif period == 'daily':
                start_time = timezone.now() - timedelta(days=7)
            elif period == 'weekly':
                start_time = timezone.now() - timedelta(weeks=4)
            else:  # monthly
                start_time = timezone.now() - timedelta(days=30)
            
            # Get trending items
            trending_items = TrendingItem.objects.filter(
                period=period,
                period_start__gte=start_time
            ).select_related('product', 'category')
            
            if category_id:
                trending_items = trending_items.filter(category_id=category_id)
            
            trending_items = trending_items.order_by('-trending_score')[:limit]
            
            serializer = TrendingItemSerializer(trending_items, many=True)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationStatsAPIView(APIView):
    """Get recommendation statistics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get recommendation performance statistics"""
        time_period = request.query_params.get('period', '7d')
        
        # Calculate time range
        if time_period == '1d':
            start_time = timezone.now() - timedelta(days=1)
        elif time_period == '7d':
            start_time = timezone.now() - timedelta(days=7)
        elif time_period == '30d':
            start_time = timezone.now() - timedelta(days=30)
        else:
            start_time = timezone.now() - timedelta(days=7)
        
        # Get user's recommendations in the period
        recommendations = UserRecommendation.objects.filter(
            user=request.user,
            created_at__gte=start_time
        )
        
        total_recommendations = recommendations.count()
        
        # Calculate rates
        click_rate = 0
        purchase_rate = 0
        feedback_rate = 0
        
        if total_recommendations > 0:
            clicks = recommendations.filter(is_clicked=True).count()
            purchases = recommendations.filter(is_purchased=True).count()
            feedback_count = RecommendationFeedback.objects.filter(
                recommendation__in=recommendations
            ).count()
            
            click_rate = (clicks / total_recommendations) * 100
            purchase_rate = (purchases / total_recommendations) * 100
            feedback_rate = (feedback_count / total_recommendations) * 100
        
        # Algorithm performance
        algorithm_stats = recommendations.values('algorithm').annotate(
            count=Count('id'),
            clicks=Count('id', filter=Q(is_clicked=True)),
            purchases=Count('id', filter=Q(is_purchased=True))
        ).order_by('-count')
        
        algorithm_performance = {}
        for stat in algorithm_stats:
            algorithm_performance[stat['algorithm']] = {
                'recommendations': stat['count'],
                'click_rate': (stat['clicks'] / stat['count'] * 100) if stat['count'] > 0 else 0,
                'purchase_rate': (stat['purchases'] / stat['count'] * 100) if stat['count'] > 0 else 0
            }
        
        # Category performance
        category_stats = recommendations.values('product__category__name').annotate(
            count=Count('id'),
            clicks=Count('id', filter=Q(is_clicked=True)),
            purchases=Count('id', filter=Q(is_purchased=True))
        ).order_by('-count')
        
        category_performance = {}
        for stat in category_stats:
            category_performance[stat['product__category__name']] = {
                'recommendations': stat['count'],
                'click_rate': (stat['clicks'] / stat['count'] * 100) if stat['count'] > 0 else 0,
                'purchase_rate': (stat['purchases'] / stat['count'] * 100) if stat['count'] > 0 else 0
            }
        
        stats_data = {
            'total_recommendations': total_recommendations,
            'click_rate': round(click_rate, 2),
            'purchase_rate': round(purchase_rate, 2),
            'feedback_rate': round(feedback_rate, 2),
            'algorithm_performance': algorithm_performance,
            'category_performance': category_performance,
            'time_period': time_period
        }
        
        serializer = RecommendationStatsSerializer(stats_data)
        return Response(serializer.data)


class UserBehaviorAPIView(APIView):
    """Track user behavior"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Record user behavior"""
        serializer = UserBehaviorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            
            # Update trending data
            behavior = serializer.instance
            self._update_trending_data(behavior)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _update_trending_data(self, behavior):
        """Update trending items based on user behavior"""
        product = behavior.product
        today = timezone.now().date()
        
        # Get or create trending item for today
        trending_item, created = TrendingItem.objects.get_or_create(
            product=product,
            period='daily',
            period_start=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0),
            defaults={
                'category': product.category,
                'period_end': timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
            }
        )
        
        # Update counts based on behavior type
        if behavior.behavior_type == 'view':
            trending_item.view_count += 1
        elif behavior.behavior_type == 'click':
            trending_item.click_count += 1
        elif behavior.behavior_type == 'purchase':
            trending_item.purchase_count += 1
        elif behavior.behavior_type == 'share':
            trending_item.share_count += 1
        
        # Calculate trending score
        trending_item.trending_score = (
            trending_item.view_count * 1 +
            trending_item.click_count * 2 +
            trending_item.purchase_count * 5 +
            trending_item.share_count * 3
        )
        
        trending_item.save()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def track_recommendation_click(request, recommendation_id):
    """Track when a user clicks on a recommendation"""
    try:
        recommendation = UserRecommendation.objects.get(
            id=recommendation_id,
            user=request.user
        )
        
        recommendation.is_clicked = True
        recommendation.clicked_at = timezone.now()
        recommendation.save()
        
        # Track behavior
        UserBehavior.objects.create(
            user=request.user,
            product=recommendation.product,
            behavior_type='click',
            session_id=request.data.get('session_id', ''),
            device_type=request.data.get('device_type', ''),
            referrer=request.data.get('referrer', '')
        )
        
        # Track history
        RecommendationHistory.objects.create(
            user=request.user,
            action_type='clicked',
            product_ids=[recommendation.product.id],
            algorithm=recommendation.algorithm
        )
        
        return Response({'status': 'success'})
    
    except UserRecommendation.DoesNotExist:
        return Response(
            {'error': 'Recommendation not found'},
            status=status.HTTP_404_NOT_FOUND
        )
