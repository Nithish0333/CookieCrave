from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, UserProfileView, ForgotPasswordView, ResetPasswordView, ResetPasswordWithCodeView, CustomLoginView, SellerProfileView, VerifySellerPhoneView, ResendSellerOTPView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-debug/', CustomLoginView.as_view(), name='custom_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password-with-code/', ResetPasswordWithCodeView.as_view(), name='reset_password_with_code'),
    path('seller-profile/', SellerProfileView.as_view(), name='seller_profile'),
    path('seller-profile/verify/', VerifySellerPhoneView.as_view(), name='verify_seller_phone'),
    path('seller-profile/resend-otp/', ResendSellerOTPView.as_view(), name='resend_seller_otp'),
]
