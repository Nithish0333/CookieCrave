import requests
import logging
import random
import string
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

def generate_otp(length=6):
    """Generate a numeric OTP of specified length."""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_sms(phone_number, otp_code):
    """
    Send OTP via Fast2SMS.
    Returns: (bool success, str message)
    """
    # Sanitize phone number (expects 10 digits)
    phone_number = ''.join(filter(str.isdigit, phone_number))
    if phone_number.startswith('91') and len(phone_number) > 10:
        phone_number = phone_number[2:]
    
    if len(phone_number) != 10:
        return False, f"Invalid phone number format: {phone_number}"

    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": settings.FAST2SMS_API_KEY.strip(),
        "Content-Type": "application/json",
    }
    
    # Use Quick SMS route ('q') as requested by user
    payload = {
        "route": "q",
        "message": f"Your CookieCrave OTP is {otp_code}. Use this to verify your account.",
        "language": "english",
        "numbers": phone_number,
    }

    try:
        logger.info(f"Sending Quick SMS (route 'q') to {phone_number}")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()
        logger.info(f"Fast2SMS Response: {data}")
        
        if data.get('return'):
            return True, "SMS sent successfully (Quick route 'q')"
        else:
            msg = data.get('message', 'Unknown error from SMS gateway')
            logger.error(f"Fast2SMS Failure: {msg}")
            return False, msg
            
    except Exception as e:
        logger.error(f"Fast2SMS Exception: {str(e)}")
        return False, str(e)
