from django.urls import path
from .views import UserDiscountListView, ClaimDiscountView, ValidateDiscountView, GetGameStatusView

urlpatterns = [
    path('my-discounts/', UserDiscountListView.as_view(), name='my-discounts'),
    path('status/', GetGameStatusView.as_view(), name='game-status'),
    path('claim/', ClaimDiscountView.as_view(), name='claim-discount'),
    path('validate/', ValidateDiscountView.as_view(), name='validate-discount'),
]
