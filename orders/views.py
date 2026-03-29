from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Users can see transactions where they are either buyer/user or the product seller
        return Transaction.objects.filter(user=user) | Transaction.objects.filter(product__seller=user)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)
        if product.seller == self.request.user:
            raise ValidationError("You cannot buy your own product.")
        total_price = product.price * quantity
        serializer.save(user=self.request.user, total_price=total_price)
