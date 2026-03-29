#!/usr/bin/env python
import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_email_configuration():
    """Test email configuration"""
    print("🔧 Testing Email Configuration...")
    print(f"📧 Email Host: {settings.EMAIL_HOST}")
    print(f"🔌 Port: {settings.EMAIL_PORT}")
    print(f"👤 From Email: {settings.EMAIL_HOST_USER}")
    print(f"🔒 TLS Enabled: {settings.EMAIL_USE_TLS}")
    print()
    
    # Check if credentials are set
    email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    
    if email == 'your-email@gmail.com' or password == 'your-app-password':
        print("❌ ERROR: Still using placeholder credentials!")
        print("📝 Please update your .env file with real Gmail credentials")
        print("📖 See setup_gmail_guide.md for instructions")
        return False
    
    print("✅ Credentials appear to be set")
    print()
    
    # Test sending email
    try:
        print("📤 Sending test email...")
        result = send_mail(
            subject='🍪 CookieCrave Email Test',
            message='''
Hello from CookieCrave!

This is a test email to verify that your Gmail configuration is working correctly.

If you receive this email, your email setup is successful! 🎉

Best regards,
CookieCrave Team
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],  # Send to self for testing
            fail_silently=False,
        )
        
        print("✅ Email sent successfully!")
        print(f"📬 Check your inbox: {email}")
        print("🎉 Gmail configuration is working!")
        return True
        
    except Exception as e:
        print(f"❌ Email failed to send: {e}")
        print()
        print("🔧 Common issues:")
        print("   • Wrong App Password (16 characters, no spaces)")
        print("   • 2-Factor Authentication not enabled")
        print("   • Firewall blocking port 587")
        print("   • Incorrect Gmail address")
        print()
        print("📖 See setup_gmail_guide.md for help")
        return False

if __name__ == "__main__":
    test_email_configuration()
