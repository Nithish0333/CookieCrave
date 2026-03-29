from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserDiscount, GamePlay
from .serializers import UserDiscountSerializer
from django.utils import timezone

class UserDiscountListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        discounts = UserDiscount.objects.filter(user=request.user, is_used=False)
        serializer = UserDiscountSerializer(discounts, many=True)
        return Response(serializer.data)

class GetGameStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        statuses = {}
        for game_type, _ in UserDiscount.GAME_CHOICES:
            play, created = GamePlay.objects.get_or_create(user=request.user, game_type=game_type)
            statuses[game_type] = {
                'can_play': play.can_play(),
                'last_played': play.last_played if not created else None
            }
        return Response(statuses)

class ClaimDiscountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        game_type = request.data.get('game_type')
        discount_percentage = request.data.get('discount')

        if not game_type or discount_percentage is None:
            return Response(
                {"error": "game_type and discount are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user can play
        play, created = GamePlay.objects.get_or_create(user=request.user, game_type=game_type)
        if not play.can_play():
            return Response(
                {"error": f"You can only play {game_type.replace('_', ' ')} once per day. Come back tomorrow!"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Record the play
        play.last_played = timezone.now()
        play.save()

        # If discount is 0, it means they played but didn't win (e.g. scratch card no match)
        # We still record the play but don't create a discount
        if int(discount_percentage) == 0:
            return Response({"message": "Play recorded, better luck next time!"})

        # Basic validation
        if int(discount_percentage) > 50: # Cap discount at 50%
            discount_percentage = 50

        discount = UserDiscount.objects.create(
            user=request.user,
            game_type=game_type,
            discount_percentage=discount_percentage
        )

        serializer = UserDiscountSerializer(discount)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ValidateDiscountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        try:
            discount = UserDiscount.objects.get(code=code, user=request.user, is_used=False)
            # Check expiration
            if discount.expires_at < timezone.now():
                return Response({"error": "Discount code has expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UserDiscountSerializer(discount)
            return Response(serializer.data)
        except UserDiscount.DoesNotExist:
            return Response({"error": "Invalid or already used discount code"}, status=status.HTTP_404_NOT_FOUND)
