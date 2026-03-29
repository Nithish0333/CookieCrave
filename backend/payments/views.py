import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.db import transaction
from .models import Payment, Order, OrderItem
from .serializers import PaymentSerializer, OrderSerializer, CreateOrderSerializer
from products.models import Product
from orders.models import Transaction, Order as LegacyOrder
from django.core.mail import send_mail
import uuid
import hmac
import hashlib


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_razorpay_order(request):
    """Create Razorpay order with optional discount code"""
    try:
        amount = request.data.get('amount')
        discount_code = request.data.get('discount_code')
        
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)

        original_amount = float(amount)
        discount_percentage = 0
        discount_id = None

        # Validate discount code if provided
        if discount_code:
            from discounts.models import UserDiscount
            from django.utils import timezone
            try:
                discount = UserDiscount.objects.get(
                    code=discount_code, 
                    user=request.user, 
                    is_used=False,
                    expires_at__gt=timezone.now()
                )
                discount_percentage = discount.discount_percentage
                discount_id = discount.id
                amount = original_amount * (1 - (discount_percentage / 100))
            except UserDiscount.DoesNotExist:
                return Response({'error': 'Invalid or expired discount code'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert to paise (Razorpay expects amount in paise)
        amount_paise = int(round(float(amount) * 100))

        # Initialize Razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        # Create Razorpay order
        razorpay_order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': f'receipt_{uuid.uuid4().hex[:8]}',
            'payment_capture': 1
        })

        # Create payment record
        payment = Payment.objects.create(
            razorpay_order_id=razorpay_order['id'],
            amount=float(amount),
            user=request.user,
            status='pending',
            payment_method='razorpay',
        )

        return Response({
            'razorpay_order_id': razorpay_order['id'],
            'amount': float(amount),
            'original_amount': original_amount,
            'discount_percentage': discount_percentage,
            'currency': 'INR',
            'key_id': settings.RAZORPAY_KEY_ID,
            'payment_id': payment.id,
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_payment(request):
    """Verify Razorpay payment and create order"""
    try:
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return Response({'error': 'Missing payment details'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get payment record
        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id, user=request.user)
        
        # Verify signature
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
        except:
            return Response({'error': 'Invalid payment signature'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update payment
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'completed'
        payment.save()
        
        return Response({
            'message': 'Payment verified successfully',
            'payment_id': payment.id
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_wholesale_payment(request):
    """Verify Razorpay payment for wholesale and send email"""
    try:
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')
        
        email = request.data.get('email')
        amount = request.data.get('amount')
        contact_name = request.data.get('contact_name')
        company = request.data.get('company', '')
        quantity = request.data.get('quantity')
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature, email, amount]):
            return Response({'error': 'Missing payment or contact details'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify signature
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
        except:
            return Response({'error': 'Invalid payment signature'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Send Email Confirmation
        email_subject = f'[CookieCrave] Advance Payment Confirmed - Wholesale Enquiry {razorpay_order_id}'
        email_body = f'''
Dear {contact_name},

Thank you for your bulk order enquiry! We have successfully received your advance payment.

Payment Details:
- Order ID: {razorpay_order_id}
- Transaction ID: {razorpay_payment_id}
- Advance Paid: ₹{amount}
- Quantity Enquired: {quantity} boxes
{f"- Company: {company}" if company else ""}

Our wholesale team is reviewing your requirements and will contact you shortly to confirm the flavours, packaging, and delivery schedule.

Best regards,
CookieCrave Wholesale Team
        '''.strip()
        
        try:
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            # We don't fail the verification if the email fails, but we print/log it.
            print(f"Failed to send email to {email}: {str(e)}")
        
        return Response({
            'message': 'Wholesale Payment verified successfully',
            'order_id': razorpay_order_id
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    """Create order after successful payment or for COD"""
    try:
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        payment_method = request.data.get('payment_method', 'razorpay')
        discount_code = request.data.get('discount_code')
        payment = None

        with transaction.atomic():
            items_data = serializer.validated_data['items']
            items_total = 0

            # Calculate base total amount from items
            for item_data in items_data:
                product = get_object_or_404(Product, id=item_data['product_id'])
                quantity = item_data['quantity']
                items_total += product.price * quantity

            final_total = items_total
            discount_obj = None

            # Apply discount if provided
            if discount_code:
                from discounts.models import UserDiscount
                try:
                    discount_obj = UserDiscount.objects.get(code=discount_code, user=request.user, is_used=False)
                    final_total = float(items_total) * (1 - (discount_obj.discount_percentage / 100))
                except UserDiscount.DoesNotExist:
                    # If discount was valid during payment creation but now missing, we might want to log this
                    pass

            if payment_method == 'razorpay':
                payment_id = request.data.get('payment_id')
                payment = get_object_or_404(
                    Payment,
                    id=payment_id,
                    user=request.user,
                    status='completed',
                    payment_method='razorpay',
                )

                # Update payment amount to the final discounted total
                payment.amount = final_total
                payment.save()
            elif payment_method == 'cod':
                # Create a payment record for COD
                payment = Payment.objects.create(
                    razorpay_order_id=f'COD{uuid.uuid4().hex[:10].upper()}',
                    amount=final_total,
                    user=request.user,
                    status='pending',
                    payment_method='cod',
                )
            else:
                return Response(
                    {'error': 'Unsupported payment method'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Mark discount as used
            if discount_obj:
                discount_obj.is_used = True
                discount_obj.save()

            # Create order
            order = Order.objects.create(
                payment=payment,
                order_id=f'ORD{uuid.uuid4().hex[:10].upper()}',
                shipping_address=serializer.validated_data['shipping_address'],
                phone_number=serializer.validated_data['phone_number']
            )

            # Create order items and transactions
            for item_data in items_data:
                product = get_object_or_404(Product, id=item_data['product_id'])
                quantity = item_data['quantity']

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                
                Transaction.objects.create(
                    user=request.user,
                    product=product,
                    quantity=quantity,
                    total_price=product.price * quantity,
                    status='completed'
                )

        return Response({
            'message': 'Order created successfully',
            'order_id': order.order_id,
            'final_amount': float(final_total)
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderListView(ListAPIView):
    """List user's orders"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(payment__user=self.request.user).order_by('-created_at')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def order_detail(request, order_id):
    """Get order details"""
    try:
        order = get_object_or_404(Order, order_id=order_id, payment__user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
