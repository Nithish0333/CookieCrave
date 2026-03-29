from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserPreference

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """Create UserPreference when a new user is created"""
    if created and not kwargs.get('raw', False):
        UserPreference.objects.get_or_create(user=instance)


@receiver(post_save, sender=UserPreference)
def clear_recommendation_cache_on_preference_change(sender, instance, **kwargs):
    """Clear recommendation cache when user preferences change"""
    from .models import RecommendationCache
    
    RecommendationCache.objects.filter(
        user=instance.user,
        is_active=True
    ).update(is_active=False)
