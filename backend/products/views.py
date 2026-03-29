from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category, Wishlist, Rating
from .serializers import ProductSerializer, CategorySerializer, WishlistSerializer, RatingSerializer
import logging

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        user_only = self.request.query_params.get('user_only')
        if user_only == 'true' and self.request.user.is_authenticated:
            return queryset.filter(seller=self.request.user)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class WishlistViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        try:
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            product_ids = request.data.get('product_ids', [])
            
            for product_id in product_ids:
                try:
                    product = Product.objects.get(id=product_id)
                    wishlist.products.add(product)
                except Product.DoesNotExist:
                    return Response({'error': f'Product {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        try:
            user = request.user
            product_id = request.data.get('product_id')
            logger.info(f'Add product request - User: {user.id}, Product: {product_id}')
            
            if not product_id:
                return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            wishlist, created = Wishlist.objects.get_or_create(user=user)
            logger.info(f'Wishlist retrieved/created - ID: {wishlist.id}, Created: {created}')
            
            try:
                product = Product.objects.get(id=product_id)
                logger.info(f'Product found - ID: {product.id}, Name: {product.name}')
                
                wishlist.products.add(product)
                wishlist.save()
                logger.info(f'Product added to wishlist successfully')
                
                serializer = WishlistSerializer(wishlist)
                logger.info(f'Wishlist serialized with {len(serializer.data.get("products", []))} products')
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                logger.error(f'Product not found - ID: {product_id}')
                return Response({'error': f'Product {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error in add_product: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def remove_product(self, request):
        try:
            user = request.user
            product_id = request.data.get('product_id')
            logger.info(f'Remove product request - User: {user.id}, Product: {product_id}')
            
            try:
                wishlist = Wishlist.objects.get(user=user)
                logger.info(f'Wishlist found - ID: {wishlist.id}')
            except Wishlist.DoesNotExist:
                logger.error(f'Wishlist not found for user {user.id}')
                return Response({'error': 'Wishlist not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if not product_id:
                return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                product = Product.objects.get(id=product_id)
                logger.info(f'Product found - ID: {product.id}, Name: {product.name}')
                
                wishlist.products.remove(product)
                wishlist.save()
                logger.info(f'Product removed from wishlist successfully')
                
                serializer = WishlistSerializer(wishlist)
                logger.info(f'Wishlist serialized with {len(serializer.data.get("products", []))} products')
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                logger.error(f'Product not found - ID: {product_id}')
                return Response({'error': f'Product {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error in remove_product: {str(e)}', exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id:
            return Rating.objects.filter(product_id=product_id)
        return Rating.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
