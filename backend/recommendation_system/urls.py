from django.urls import path
from . import views

app_name = 'recommendation_system'

urlpatterns = [
    # Main recommendation endpoints
    path('recommendations/', views.RecommendationAPIView.as_view(), name='recommendations'),
    path('recommendations/<int:recommendation_id>/click/', 
         views.track_recommendation_click, name='track_recommendation_click'),
    
    # Feedback endpoints
    path('feedback/', views.RecommendationFeedbackAPIView.as_view(), name='feedback'),
    
    # User preferences
    path('preferences/', views.UserPreferenceAPIView.as_view(), name='preferences'),
    
    # Trending items
    path('trending/', views.TrendingItemsAPIView.as_view(), name='trending'),
    
    # Statistics
    path('stats/', views.RecommendationStatsAPIView.as_view(), name='stats'),
    
    # User behavior tracking
    path('behavior/', views.UserBehaviorAPIView.as_view(), name='behavior'),
]
