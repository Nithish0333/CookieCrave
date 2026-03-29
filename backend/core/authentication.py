from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class SilentJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that does NOT raise exceptions for invalid/expired tokens.
    Instead, it returns None (unauthenticated) silently, allowing AllowAny endpoints
    to work even when the client sends an invalid or expired Bearer token.
    """

    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (InvalidToken, TokenError):
            return None
