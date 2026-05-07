from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .serializers import UserSerializer, SellerProfileSerializer
from .models import User, SellerProfile
import logging
import requests
import string
import random
from django.conf import settings
from django.utils import timezone
from .sms_utils import generate_otp, send_otp_sms

logger = logging.getLogger(__name__)

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Registration attempt with data: {request.data}")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists for security
            return Response({'detail': 'If an account exists with this email, a verification code has been sent.'}, status=status.HTTP_200_OK)
        
        # Generate token and verification code
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_code = generate_otp()
        
        user.reset_verification_code = verification_code
        user.reset_otp_created_at = timezone.now()
        user.save()
        
        # Create reset link (you can customize this URL)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/?code={verification_code}"
        
        # Send email using direct SMTP (working method)
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            logger.info(f"Attempting to send password reset email to: {email}")
            logger.info(f"Generated verification code: {verification_code}")
            
            email_subject = f'[CookieCrave] Password Reset - Verification Code: {verification_code}'
            email_body = f'''
You requested a password reset for your CookieCrave account.

Your verification code is: {verification_code}

You can also click the link below to reset your password:
{reset_link}

This verification code and link will expire in 24 hours.

If you did not request this reset, please ignore this email.

For security, please:
1. Never share this verification code
2. CookieCrave staff will never ask for your password
3. Only enter this code on the official CookieCrave website
            '''.strip()
            
            # Create email message
            msg = MIMEText(email_body)
            msg['Subject'] = email_subject
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['To'] = email
            
            # Send via direct SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Password reset email sent successfully to: {email}")
            
            return Response({
                'detail': 'Password reset verification code sent to your email.',
                'verification_code_sent': True,
                'email_hint': f'Code sent to {email[:2]}***@{email.split("@")[1]}'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Email sending error: {str(e)}", exc_info=True)
            logger.error(f"Email settings - Host: {settings.EMAIL_HOST}, Port: {settings.EMAIL_PORT}, User: {settings.EMAIL_HOST_USER}")
            
            # Try alternative email service or provide clear error message
            error_msg = str(e)
            if 'authentication' in error_msg.lower() or 'login' in error_msg.lower():
                return Response({'detail': 'Email authentication failed. Please check Gmail credentials.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif 'connection' in error_msg.lower():
                return Response({'detail': 'Email connection failed. Please check internet connection.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'detail': f'Email sending failed: {error_msg}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid or expired reset link.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get verification code from query parameters or request body
        verification_code = request.GET.get('code') or request.data.get('verification_code')

        new_password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        retyped_password = request.data.get('retyped_password')

        if not new_password or not confirm_password or not retyped_password:
            return Response({'detail': 'All password fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'detail': 'New password and confirm password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != retyped_password:
            return Response({'detail': 'Password and retype password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({'detail': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate verification code
        if user.reset_verification_code != verification_code:
            return Response({'detail': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check for expiration (10 minutes)
        if user.reset_otp_created_at:
            time_diff = timezone.now() - user.reset_otp_created_at
            if time_diff.total_seconds() > 600: # 10 minutes
                return Response({'detail': 'Verification code has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.reset_verification_code = ''
        user.reset_otp_created_at = None
        user.set_password(new_password)
        user.save()

        # Send confirmation email
        try:
            send_mail(
                'Password Reset Successful',
                f'''
Your password for CookieCrave account ({user.email}) has been successfully reset.

If you did not make this change, please contact support immediately.

Security Tips:
1. Use a strong, unique password
2. Enable two-factor authentication if available
3. Never share your password with anyone
                '''.strip(),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Confirmation email error: {str(e)}", exc_info=True)

        return Response({
            'detail': 'Password reset successful. You can now login with your new password.',
            'password_reset': True
        }, status=status.HTTP_200_OK)

class ResetPasswordWithCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        new_password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        retyped_password = request.data.get('retyped_password')

        if not email or not verification_code or not new_password or not confirm_password or not retyped_password:
            return Response({'detail': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'detail': 'New password and confirm password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != retyped_password:
            return Response({'detail': 'Password and retype password do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({'detail': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            logger.info(f"Found user: {user.username} for email: {email}")
            
            # Validate verification code
            if user.reset_verification_code != verification_code:
                return Response({'detail': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
                
            # Check for expiration (10 minutes)
            if user.reset_otp_created_at:
                time_diff = timezone.now() - user.reset_otp_created_at
                if time_diff.total_seconds() > 600: # 10 minutes
                    return Response({'detail': 'Verification code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

            # Use database transaction to ensure atomic operation
            from django.db import transaction
            with transaction.atomic():
                user.reset_verification_code = ''
                user.reset_otp_created_at = None
                user.set_password(new_password)
                user.save()
                logger.info(f"Password updated for user: {user.username}")
                
                # Verify password was set correctly immediately
                user.refresh_from_db()
                if user.check_password(new_password):
                    logger.info("Password verification successful")
                else:
                    logger.error("Password verification failed after setting")
                    raise Exception("Password was not set correctly")

            # Send confirmation email
            send_mail(
                'Password Reset Successful',
                f'''
Your password for CookieCrave account ({email}) has been successfully reset.

If you did not make this change, please contact support immediately.

Security Tips:
1. Use a strong, unique password
2. Enable two-factor authentication if available
3. Never share your password with anyone
                '''.strip(),
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return Response({
                'detail': 'Password reset successful. You can now login with your new password.',
                'password_reset': True
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'detail': 'Invalid email or verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}", exc_info=True)
            return Response({'detail': 'Error resetting password. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        logger.info(f"Login attempt for username: {username}")
        
        try:
            user = User.objects.get(username=username)
            logger.info(f"Found user: {user.username}")
            
            if user.check_password(password):
                logger.info("Password verification successful for login")
                # Generate tokens using the same logic as JWT
                from rest_framework_simplejwt.tokens import RefreshToken
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                
                logger.info("Tokens generated successfully")
                return Response({
                    'access': str(access),
                    'refresh': str(refresh)
                })
            else:
                logger.error("Password verification failed for login")
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                
        except User.DoesNotExist:
            logger.error(f"User not found: {username}")
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return Response({'detail': 'Error during login'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class SellerProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.seller_profile
            serializer = SellerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SellerProfile.DoesNotExist:
            return Response({'detail': 'Seller profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if hasattr(request.user, 'seller_profile'):
            profile = request.user.seller_profile
            if profile.phone_verified:
                return Response({'detail': 'Seller profile already exists and is verified.'}, status=status.HTTP_400_BAD_REQUEST)
            # If not verified, we might want to allow re-sending OTP or updating details?
            # For now, let's delete the unverified profile to allow a fresh start.
            profile.delete()
        
        serializer = SellerProfileSerializer(data=request.data)
        if serializer.is_valid():
            raw_phone_number = serializer.validated_data.get('phone_number', '')
            # Sanitize phone number for Fast2SMS (expects 10 digits usually)
            phone_number = ''.join(filter(str.isdigit, raw_phone_number))
            if phone_number.startswith('91') and len(phone_number) > 10:
                phone_number = phone_number[2:]
            
            if not phone_number or len(phone_number) < 10:
                return Response({'detail': f'Invalid phone number: {raw_phone_number}. Please provide a 10-digit number.'}, status=status.HTTP_400_BAD_REQUEST)
            
            verification_code = generate_otp()
            
            sms_success, last_error = send_otp_sms(phone_number, verification_code)

            if not sms_success:
                logger.error(f"Fast2SMS failed for {phone_number}: {last_error}")
                print(f"\n[CRITICAL ERROR] Fast2SMS failed for {phone_number}: {last_error}")
                print(f"[DEBUG] OTP for {phone_number}: {verification_code}\n")

            serializer.save(
                user=request.user, 
                phone_verified=False, 
                verification_code=verification_code,
                otp_created_at=timezone.now()
            )
            return Response({
                'detail': 'Verification code sent to your phone.',
                'requires_verification': True,
                'phone_number': phone_number,
                'debug_msg': None if sms_success else f"Service error: {last_error}. (Check terminal if testing)"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifySellerPhoneView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'detail': 'Verification code is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            profile = request.user.seller_profile
            if profile.phone_verified:
                return Response({'detail': 'Phone already verified.'}, status=status.HTTP_200_OK)
            
            if profile.verification_code == code:
                # Check for expiration (10 minutes)
                if profile.otp_created_at:
                    time_diff = timezone.now() - profile.otp_created_at
                    if time_diff.total_seconds() > 600: # 10 minutes
                        return Response({'detail': 'Verification code has expired. Please request a new one.'}, status=status.HTTP_400_BAD_REQUEST)

                profile.phone_verified = True
                profile.verification_code = ''
                profile.otp_created_at = None
                profile.save()
                return Response({'detail': 'Phone verified successfully. You are now a registered seller!'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        except SellerProfile.DoesNotExist:
            return Response({'detail': 'Seller profile not found. Please register first.'}, status=status.HTTP_404_NOT_FOUND)

class ResendSellerOTPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            profile = request.user.seller_profile
            if profile.phone_verified:
                return Response({'detail': 'Phone already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            
            phone_number = profile.phone_number
            # Sanitize
            phone_number = ''.join(filter(str.isdigit, phone_number))
            if phone_number.startswith('91') and len(phone_number) > 10:
                phone_number = phone_number[2:]
            
            # Rate limiting: check if last OTP was sent too recently (60 seconds)
            if profile.otp_created_at:
                time_since_last = timezone.now() - profile.otp_created_at
                if time_since_last.total_seconds() < 60:
                    wait_time = int(60 - time_since_last.total_seconds())
                    return Response({'detail': f'Please wait {wait_time} seconds before requesting another code.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            # Generate new OTP only once
            verification_code = generate_otp()
            profile.verification_code = verification_code
            profile.otp_created_at = timezone.now()
            profile.save()

            sms_success, last_error = send_otp_sms(phone_number, verification_code)

            if not sms_success:
                logger.error(f"Resend Fast2SMS failed: {last_error}")
                print(f"[DEBUG] Resend OTP for {phone_number}: {verification_code}")

            return Response({
                'detail': 'Verification code resent to your phone.',
                'requires_verification': True,
                'phone_number': phone_number,
                'debug_msg': None if sms_success else f"Service error: {last_error}. (Check terminal if testing)"
            }, status=status.HTTP_200_OK)

        except SellerProfile.DoesNotExist:
            return Response({'detail': 'Registration profile not found.'}, status=status.HTTP_404_NOT_FOUND)
