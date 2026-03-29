from django.apps import AppConfig


class RecommendationSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommendation_system'
    verbose_name = 'Recommendation System'
    
    def ready(self):
        """Import signal handlers when app is ready"""
        try:
            from . import signals
        except ImportError:
            pass
