from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from analytics.views_admin import analytics_dashboard_view
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/analytics/', analytics_dashboard_view, name='analytics_dashboard'),
    path('api/users/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api/', include('orders.urls')),
    path('api/', include('payments.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/recommendations/', include('recommendation_system.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/discounts/', include('discounts.urls')),
    path('', views.index_view, name='index'),  # Move to end
    # Custom media serving with CORS
    path('media/<path:file_path>', views.serve_media_with_cors, name='serve_media'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
