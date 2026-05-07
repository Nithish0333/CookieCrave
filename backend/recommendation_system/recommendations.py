from django.db.models import Count, Q, Avg, F, Window
from django.db.models.functions import RowNumber
from django.utils import timezone
from datetime import timedelta
import random
import math
from collections import defaultdict, Counter
from .models import (
    UserPreference, UserRecommendation, UserBehavior, 
    TrendingItem, RecommendationCache
)
from products.models import Product, Category


class RecommendationEngine:
    """Netflix-style recommendation engine with multiple algorithms"""
    
    def __init__(self, user):
        self.user = user
        self.preferences, created = UserPreference.objects.get_or_create(user=user)
        
    def get_recommendations(self, algorithm='hybrid', limit=20, exclude_purchased=True):
        """Get recommendations using specified algorithm"""
        algorithms = {
            'personalized': self._personalized_recommendations,
            'collaborative': self._collaborative_filtering,
            'content_based': self._content_based_recommendations,
            'popularity': self._popularity_based_recommendations,
            'seasonal': self._seasonal_recommendations,
            'trending': self._trending_recommendations,
            'hybrid': self._hybrid_recommendations
        }
        
        if algorithm not in algorithms:
            algorithm = 'hybrid'
            
        # Check cache first
        cache_key = f"{algorithm}_{limit}_{exclude_purchased}"
        cached = self._get_cached_recommendations(cache_key)
        if cached:
            return cached
            
        recommendations = algorithms[algorithm](limit, exclude_purchased)
        
        # Cache the results
        self._cache_recommendations(cache_key, algorithm, recommendations)
        
        return recommendations
    
    def _personalized_recommendations(self, limit=20, exclude_purchased=True):
        """Based on user's viewing history and preferences"""
        # Get user's behavior patterns
        user_behaviors = UserBehavior.objects.filter(
            user=self.user
        ).select_related('product')
        
        # Calculate category preferences from behavior
        category_scores = defaultdict(float)
        product_scores = defaultdict(float)
        
        for behavior in user_behaviors:
            weight = self._get_behavior_weight(behavior.behavior_type)
            category_scores[behavior.product.category.id] += weight
            product_scores[behavior.product.id] += weight
        
        # Get products from preferred categories
        preferred_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        category_ids = [cat_id for cat_id, score in preferred_categories if score > 0]
        
        if not category_ids:
            return self._fallback_recommendations(limit)
        
        products = Product.objects.filter(
            category__id__in=category_ids,
            stock__gt=0
        ).exclude(
            id__in=product_scores.keys()
        )
        
        if exclude_purchased:
            purchased_products = UserBehavior.objects.filter(
                user=self.user, behavior_type='purchase'
            ).values_list('product_id', flat=True)
            products = products.exclude(id__in=purchased_products)
        
        # Score products based on category preference and other factors
        scored_products = []
        for product in products:
            score = category_scores.get(product.category.id, 0)
            
            # Apply user preference adjustments
            if product.category.id in self.preferences.category_preferences:
                score *= (1 + self.preferences.category_preferences[product.category.id])
            
            # Price sensitivity adjustment
            if self.preferences.price_sensitivity > 0.7:
                # User is price sensitive, prefer cheaper items
                max_price = Product.objects.filter(category=product.category).aggregate(
                    avg_price=Avg('price')
                )['avg_price'] or product.price
                if product.price < max_price:
                    score *= 1.2
            
            scored_products.append((product, score))
        
        # Sort by score and limit
        scored_products.sort(key=lambda x: x[1], reverse=True)
        return [product for product, score in scored_products[:limit]]
    
    def _collaborative_filtering(self, limit=20, exclude_purchased=True):
        """Based on similar users' behavior"""
        # Find users with similar behavior patterns
        user_categories = UserBehavior.objects.filter(
            user=self.user
        ).values_list('product__category_id', flat=True).distinct()
        
        # Find users who interacted with same categories
        similar_users = UserBehavior.objects.filter(
            product__category_id__in=user_categories
        ).exclude(user=self.user).values_list('user_id', flat=True).distinct()
        
        if not similar_users:
            return self._fallback_recommendations(limit)
        
        # Get products liked by similar users
        similar_behaviors = UserBehavior.objects.filter(
            user_id__in=similar_users,
            behavior_type__in=['purchase', 'click', 'add_to_cart']
        ).select_related('product')
        
        # Score products based on similar user interactions
        product_scores = defaultdict(float)
        for behavior in similar_behaviors:
            weight = self._get_behavior_weight(behavior.behavior_type)
            product_scores[behavior.product.id] += weight
        
        # Remove products user already interacted with
        user_products = UserBehavior.objects.filter(
            user=self.user
        ).values_list('product_id', flat=True)
        
        recommended_products = Product.objects.filter(
            id__in=product_scores.keys(),
            stock__gt=0
        ).exclude(id__in=user_products)
        
        if exclude_purchased:
            purchased_products = UserBehavior.objects.filter(
                user=self.user, behavior_type='purchase'
            ).values_list('product_id', flat=True)
            recommended_products = recommended_products.exclude(id__in=purchased_products)
        
        # Sort by score
        scored_products = [(product, product_scores[product.id]) for product in recommended_products]
        scored_products.sort(key=lambda x: x[1], reverse=True)
        
        return [product for product, score in scored_products[:limit]]
    
    def _content_based_recommendations(self, limit=20, exclude_purchased=True):
        """Based on user's favorite categories and preferences"""
        # Use user's explicit preferences
        category_preferences = self.preferences.category_preferences
        
        if not category_preferences:
            return self._fallback_recommendations(limit)
        
        # Get products from preferred categories
        preferred_categories = sorted(
            category_preferences.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        category_ids = [cat_id for cat_id, score in preferred_categories if score > 0.3]
        
        if not category_ids:
            return self._fallback_recommendations(limit)
        
        products = Product.objects.filter(
            category__id__in=category_ids,
            stock__gt=0
        )
        
        if exclude_purchased:
            purchased_products = UserBehavior.objects.filter(
                user=self.user, behavior_type='purchase'
            ).values_list('product_id', flat=True)
            products = products.exclude(id__in=purchased_products)
        
        # Score products based on preferences
        scored_products = []
        for product in products:
            score = category_preferences.get(product.category.id, 0)
            
            # Apply novelty preference
            if self.preferences.novelty_seeking > 0.7:
                # User likes new things, boost newer products
                days_old = (timezone.now() - product.created_at).days
                if days_old < 30:
                    score *= (1 + (30 - days_old) / 30)
            
            scored_products.append((product, score))
        
        scored_products.sort(key=lambda x: x[1], reverse=True)
        return [product for product, score in scored_products[:limit]]
    
    def _popularity_based_recommendations(self, limit=20, exclude_purchased=True):
        """Based on overall product popularity"""
        # Calculate popularity scores from behaviors
        popularity_scores = UserBehavior.objects.filter(
            behavior_type__in=['purchase', 'click', 'add_to_cart']
        ).values('product_id').annotate(
            score=Count('id') + Count('id', filter=Q(behavior_type='purchase')) * 3
        ).order_by('-score')[:limit*2]
        
        product_ids = [item['product_id'] for item in popularity_scores]
        
        products = Product.objects.filter(
            id__in=product_ids,
            stock__gt=0
        )
        
        if exclude_purchased:
            purchased_products = UserBehavior.objects.filter(
                user=self.user, behavior_type='purchase'
            ).values_list('product_id', flat=True)
            products = products.exclude(id__in=purchased_products)
        
        # Maintain popularity order
        product_dict = {p.id: p for p in products}
        ordered_products = []
        for item in popularity_scores:
            if item['product_id'] in product_dict:
                ordered_products.append(product_dict[item['product_id']])
                if len(ordered_products) >= limit:
                    break
        
        return ordered_products[:limit]
    
    def _seasonal_recommendations(self, limit=20, exclude_purchased=True):
        """Based on current season/time of year"""
        current_month = timezone.now().month
        
        # Define seasonal preferences
        seasonal_categories = {
            'winter': [12, 1, 2],  # Warm, spicy cookies
            'spring': [3, 4, 5],   # Light, floral cookies
            'summer': [6, 7, 8],   # Fruity, light cookies
            'fall': [9, 10, 11],   # Pumpkin, spice cookies
        }
        
        season = None
        for season_name, months in seasonal_categories.items():
            if current_month in months:
                season = season_name
                break
        
        if not season:
            return self._fallback_recommendations(limit)
        
        # Use user's seasonal preferences if available
        seasonal_prefs = self.preferences.seasonal_preferences.get(season, {})
        
        if seasonal_prefs:
            category_ids = [cat_id for cat_id, score in seasonal_prefs.items() if score > 0.5]
            if category_ids:
                products = Product.objects.filter(
                    category__id__in=category_ids,
                    stock__gt=0
                )
            else:
                products = Product.objects.filter(stock__gt=0)
        else:
            # Fallback to all products with seasonal boost
            products = Product.objects.filter(stock__gt=0)
        
        if exclude_purchased:
            purchased_products = UserBehavior.objects.filter(
                user=self.user, behavior_type='purchase'
            ).values_list('product_id', flat=True)
            products = products.exclude(id__in=purchased_products)
        
        # Add seasonal randomness
        products_list = list(products)
        random.shuffle(products_list)
        
        return products_list[:limit]
    
    def _trending_recommendations(self, limit=20, exclude_purchased=True):
        """Based on recent activity patterns"""
        # Get trending items from the last 7 days
        week_ago = timezone.now() - timedelta(days=7)
        
        trending_products = TrendingItem.objects.filter(
            period='daily',
            period_start__gte=week_ago
        ).select_related('product').order_by('-trending_score')[:limit*2]
        
        products = [item.product for item in trending_products if item.product.stock > 0]
        
        if exclude_purchased:
            purchased_products = UserBehavior.objects.filter(
                user=self.user, behavior_type='purchase'
            ).values_list('product_id', flat=True)
            products = [p for p in products if p.id not in purchased_products]
        
        return products[:limit]
    
    def _hybrid_recommendations(self, limit=20, exclude_purchased=True):
        """Combination of multiple algorithms"""
        algorithms = [
            ('personalized', 0.3),
            ('collaborative', 0.25),
            ('content_based', 0.2),
            ('trending', 0.15),
            ('popularity', 0.1)
        ]
        
        all_recommendations = defaultdict(float)
        
        for algo_name, weight in algorithms:
            try:
                recs = self.get_recommendations(algo_name, limit*2, exclude_purchased)
                for i, product in enumerate(recs):
                    # Higher position gets higher score
                    position_score = 1.0 - (i / len(recs))
                    all_recommendations[product.id] += weight * position_score
            except:
                continue
        
        # Sort by combined score
        sorted_products = sorted(
            all_recommendations.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        product_ids = [pid for pid, score in sorted_products[:limit*2]]
        products = Product.objects.filter(id__in=product_ids, stock__gt=0)
        
        # Maintain order
        product_dict = {p.id: p for p in products}
        ordered_products = []
        for pid in product_ids:
            if pid in product_dict and len(ordered_products) < limit:
                ordered_products.append(product_dict[pid])
        
        return ordered_products
    
    def _fallback_recommendations(self, limit=20):
        """Fallback recommendations when no data is available"""
        # Return random popular products
        return Product.objects.filter(stock__gt=0).order_by('?')[:limit]
    
    def _get_behavior_weight(self, behavior_type):
        """Get weight for different behavior types"""
        weights = {
            'view': 1,
            'click': 2,
            'add_to_cart': 3,
            'purchase': 5,
            'review': 4,
            'share': 3,
            'wishlist': 3
        }
        return weights.get(behavior_type, 1)
    
    def _get_cached_recommendations(self, cache_key):
        """Get recommendations from cache"""
        try:
            cached = RecommendationCache.objects.get(
                user=self.user,
                cache_key=cache_key,
                is_active=True,
                expires_at__gt=timezone.now()
            )
            
            # Update hit count and last accessed
            cached.hit_count += 1
            cached.last_accessed = timezone.now()
            cached.save()
            
            product_ids = cached.product_data.get('product_ids', [])
            return Product.objects.filter(id__in=product_ids, stock__gt=0)
        except RecommendationCache.DoesNotExist:
            return None
    
    def _cache_recommendations(self, cache_key, algorithm, recommendations):
        """Cache recommendations for future use"""
        expires_at = timezone.now() + timedelta(hours=1)  # Cache for 1 hour
        
        RecommendationCache.objects.update_or_create(
            user=self.user,
            cache_key=cache_key,
            defaults={
                'algorithm': algorithm,
                'product_data': {
                    'product_ids': [p.id for p in recommendations],
                    'count': len(recommendations)
                },
                'expires_at': expires_at,
                'is_active': True
            }
        )
    
    def record_feedback(self, recommendation_id, feedback_type, rating=None, comment=''):
        """Record user feedback on recommendations"""
        try:
            recommendation = UserRecommendation.objects.get(
                id=recommendation_id,
                user=self.user
            )
            
            # Update recommendation based on feedback
            if feedback_type == 'like':
                self._update_preferences_from_feedback(recommendation.product, positive=True)
            elif feedback_type == 'dislike':
                self._update_preferences_from_feedback(recommendation.product, positive=False)
            
            # Create feedback record
            from .models import RecommendationFeedback
            feedback = RecommendationFeedback.objects.create(
                recommendation=recommendation,
                user=self.user,
                feedback_type=feedback_type,
                rating=rating,
                comment=comment
            )
            
            return feedback
        except UserRecommendation.DoesNotExist:
            return None
    
    def _update_preferences_from_feedback(self, product, positive=True):
        """Update user preferences based on feedback"""
        category_id = product.category.id
        
        if positive:
            # Increase preference for this category
            current_pref = self.preferences.category_preferences.get(str(category_id), 0.5)
            new_pref = min(1.0, current_pref + 0.1)
            self.preferences.category_preferences[str(category_id)] = new_pref
        else:
            # Decrease preference for this category
            current_pref = self.preferences.category_preferences.get(str(category_id), 0.5)
            new_pref = max(0.0, current_pref - 0.1)
            self.preferences.category_preferences[str(category_id)] = new_pref
        
        self.preferences.save()
