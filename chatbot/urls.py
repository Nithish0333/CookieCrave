from django.urls import path

from .views import ChatbotView, ChatbotAnalyticsView

urlpatterns = [
    path('', ChatbotView.as_view(), name='chatbot'),
    path('analytics/', ChatbotAnalyticsView.as_view(), name='chatbot_analytics'),
]

