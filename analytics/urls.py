from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserBehaviorViewSet, UserSessionViewSet, 
    HeatmapDataViewSet, track_event
)

router = DefaultRouter()
router.register(r'behaviors', UserBehaviorViewSet, basename='userbehavior')
router.register(r'sessions', UserSessionViewSet, basename='usersession')
router.register(r'heatmap', HeatmapDataViewSet, basename='heatmap')

urlpatterns = [
    path('', include(router.urls)),
    path('track/', track_event, name='track_event'),
]
