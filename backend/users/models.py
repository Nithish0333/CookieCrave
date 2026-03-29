from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    cookie_balance = models.PositiveIntegerField(default=100)
    reset_verification_code = models.CharField(max_length=6, blank=True)
    reset_otp_created_at = models.DateTimeField(null=True, blank=True)

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    phone_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.business_name}"
