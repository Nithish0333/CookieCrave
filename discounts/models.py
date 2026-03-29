from django.db import models
from django.conf import settings
from django.utils import timezone
import random
import string

class UserDiscount(models.Model):
    GAME_CHOICES = [
        ('scratch_card', 'Scratch Card'),
        ('memory_match', 'Memory Match'),
        ('spin_wheel', 'Spin the Wheel'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='discounts'
    )
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.PositiveIntegerField()
    game_type = models.CharField(max_length=20, choices=GAME_CHOICES)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

    def generate_code(self):
        prefix = "CC" # CookieCrave
        chars = string.ascii_uppercase + string.digits
        random_str = ''.join(random.choices(chars, k=6))
        return f"{prefix}-{random_str}-{self.discount_percentage}"

    def __str__(self):
        return f"{self.user.username} - {self.code} ({self.discount_percentage}%)"

class GamePlay(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='game_plays'
    )
    game_type = models.CharField(max_length=20, choices=UserDiscount.GAME_CHOICES)
    last_played = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'game_type']

    def can_play(self):
        if not self.last_played:
            return True
        return self.last_played.date() < timezone.now().date()

    def __str__(self):
        return f"{self.user.username} played {self.game_type} on {self.last_played}"
