
# FIX FOR ResendSellerOTPView in backend/users/views.py

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

            # Generate new OTP (FIXED: use generate_otp, not generate_verification_code)
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
            return Response({'detail': 'Seller profile not found. Please register first.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Resend OTP error: {str(e)}", exc_info=True)
            return Response({'detail': 'Error resending verification code.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    