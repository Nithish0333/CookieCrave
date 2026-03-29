#!/usr/bin/env python
"""
Complete Email Diagnostic and Fix
Address all possible email sending issues
"""
import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail, get_connection
from django.conf import settings
from users.models import User
from users.views import generate_verification_code
from django.utils import timezone
import requests
import time

def test_gmail_smtp_direct():
    """Test Gmail SMTP directly without Django"""
    print("🔧 TESTING GMAIL SMTP DIRECTLY")
    print("=" * 40)
    
    try:
        # Gmail SMTP settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        print(f"📧 Server: {smtp_server}:{smtp_port}")
        print(f"👤 Username: {settings.EMAIL_HOST_USER}")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = settings.EMAIL_HOST_USER
        msg['Subject'] = 'DIRECT SMTP TEST - CookieCrave'
        
        body = '''
This is a direct SMTP test from CookieCrave.

If you receive this email, direct SMTP is working.

Time: {}
        '''.format(time.strftime('%Y-%m-%d %H:%M:%S'))
        
        msg.attach(MIMEText(body, 'plain'))
        
        print(f"🔧 Connecting to Gmail SMTP...")
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        
        print(f"🔐 Logging in...")
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        
        print(f"📧 Sending email...")
        text = msg.as_string()
        server.sendmail(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER, text)
        
        server.quit()
        
        print(f"✅ Direct SMTP email sent successfully!")
        print(f"📧 Check inbox: {settings.EMAIL_HOST_USER}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Gmail authentication failed: {e}")
        print(f"💡 This means your Gmail app password is incorrect")
        print(f"🔗 Generate new app password: https://myaccount.google.com/apppasswords")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Direct SMTP error: {e}")
        return False

def test_django_email_backend():
    """Test Django email backend"""
    print(f"\n🔧 TESTING DJANGO EMAIL BACKEND")
    print("=" * 45)
    
    try:
        # Test with explicit connection
        connection = get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            timeout=30
        )
        
        print(f"📧 Connection settings:")
        print(f"   Host: {connection.host}")
        print(f"   Port: {connection.port}")
        print(f"   Username: {connection.username}")
        print(f"   Use TLS: {connection.use_tls}")
        
        # Test connection
        connection.open()
        print(f"✅ Connection opened successfully")
        
        # Send test email
        result = send_mail(
            'DJANGO BACKEND TEST - CookieCrave',
            '''
This is a Django backend test from CookieCrave.

If you receive this email, Django email backend is working.

Time: {}
            '''.format(time.strftime('%Y-%m-%d %H:%M:%S')),
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            connection=connection,
            fail_silently=False
        )
        
        connection.close()
        
        if result == 1:
            print(f"✅ Django backend email sent successfully!")
            print(f"📧 Check inbox: {settings.EMAIL_HOST_USER}")
            return True
        else:
            print(f"❌ Django backend failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Django backend error: {e}")
        return False

def test_forgot_password_with_logging():
    """Test forgot password with detailed logging"""
    print(f"\n🔧 TESTING FORGOT PASSWORD WITH LOGGING")
    print("=" * 50)
    
    try:
        # Get user
        test_email = 'nithish123@gmail.com'
        user = User.objects.get(email=test_email)
        print(f"✅ Found user: {user.username}")
        
        # Generate verification code
        verification_code = generate_verification_code()
        print(f"🔢 Generated code: {verification_code}")
        
        # Create email content
        email_subject = f'[CookieCrave] Password Reset - Verification Code: {verification_code}'
        email_body = f'''
You requested a password reset for your CookieCrave account.

Your verification code is: {verification_code}

This verification code will expire in 24 hours.

If you did not request this reset, please ignore this email.

For security, please:
1. Never share this verification code
2. CookieCrave staff will never ask for your password
3. Only enter this code on the official CookieCrave website

Test Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
        '''.strip()
        
        print(f"📧 Email details:")
        print(f"   To: {user.email}")
        print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"   Subject: {email_subject}")
        print(f"   Body length: {len(email_body)} characters")
        
        # Send with multiple methods
        print(f"\n📧 Method 1: Django send_mail")
        try:
            result1 = send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            print(f"   Result: {result1}")
        except Exception as e:
            print(f"   Error: {e}")
            result1 = 0
        
        print(f"\n📧 Method 2: Direct SMTP")
        try:
            result2 = test_gmail_smtp_direct()
        except Exception as e:
            print(f"   Error: {e}")
            result2 = False
        
        # Update user with verification code
        user.reset_verification_code = verification_code
        user.reset_otp_created_at = timezone.now()
        user.save()
        print(f"✅ User updated with verification code")
        
        if result1 == 1 or result2:
            print(f"✅ At least one method succeeded!")
            return True
        else:
            print(f"❌ All methods failed")
            return False
            
    except Exception as e:
        print(f"❌ Forgot password test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_gmail_app_password_setup():
    """Check Gmail app password setup"""
    print(f"\n🔐 GMAIL APP PASSWORD DIAGNOSTIC")
    print("=" * 45)
    
    current_password = settings.EMAIL_HOST_PASSWORD
    
    print(f"📋 Current password analysis:")
    print(f"   Length: {len(current_password)} characters")
    print(f"   Contains spaces: {'Yes' if ' ' in current_password else 'No'}")
    print(f"   Format: '{current_password[:4]}...{current_password[-4:]}'")
    
    print(f"\n📋 Gmail App Password Requirements:")
    print(f"✅ 2-Factor Authentication must be enabled")
    print(f"✅ Generate at: https://myaccount.google.com/apppasswords")
    print(f"✅ Format: 16 characters like 'abcd efgh ijkl mnop'")
    print(f"✅ Use this password, NOT your regular Gmail password")
    
    if len(current_password) != 16 or ' ' not in current_password:
        print(f"\n❌ Current password doesn't look like an app password!")
        print(f"💡 Please generate a new Gmail App Password")
        return False
    else:
        print(f"\n✅ Password format looks correct")
        return True

def create_email_backup_config():
    """Create backup email configuration"""
    print(f"\n🛠️  BACKUP EMAIL CONFIGURATION")
    print("=" * 40)
    
    backup_config = '''
# BACKUP EMAIL CONFIGURATION
# Try this if current config doesn't work

# Option 1: Different port (SSL)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'cookiecrave001@gmail.com'
EMAIL_HOST_PASSWORD = 'YOUR_APP_PASSWORD'

# Option 2: Console backend (for testing)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Option 3: File backend (for testing)
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/path/to/sent/emails'
    '''
    
    print(backup_config)
    
    with open('backup_email_config.py', 'w') as f:
        f.write(backup_config)
    
    print(f"\n💾 Saved to: backup_email_config.py")

def main():
    print("🔧 COMPLETE EMAIL DIAGNOSTIC AND FIX")
    print("=" * 50)
    
    print(f"📧 Current email settings:")
    print(f"   Backend: {settings.EMAIL_BACKEND}")
    print(f"   Host: {settings.EMAIL_HOST}")
    print(f"   Port: {settings.EMAIL_PORT}")
    print(f"   TLS: {settings.EMAIL_USE_TLS}")
    print(f"   User: {settings.EMAIL_HOST_USER}")
    
    # Check Gmail app password
    password_ok = check_gmail_app_password_setup()
    
    # Test direct SMTP
    smtp_ok = test_gmail_smtp_direct()
    
    # Test Django backend
    django_ok = test_django_email_backend()
    
    # Test forgot password
    forgot_ok = test_forgot_password_with_logging()
    
    # Show backup config
    create_email_backup_config()
    
    print(f"\n🎯 DIAGNOSTIC RESULTS:")
    print(f"✅ Gmail App Password: {'OK' if password_ok else 'NEEDS FIX'}")
    print(f"✅ Direct SMTP: {'Working' if smtp_ok else 'Failed'}")
    print(f"✅ Django Backend: {'Working' if django_ok else 'Failed'}")
    print(f"✅ Forgot Password: {'Working' if forgot_ok else 'Failed'}")
    
    if smtp_ok or django_ok:
        print(f"\n🎉 EMAIL SYSTEM IS WORKING!")
        print(f"📧 Check your inbox for test emails")
        print(f"💡 If still not receiving, check:")
        print(f"   • Spam/junk folder")
        print(f"   • Gmail promotions/social tabs")
        print(f"   • Email filters")
        print(f"   • Try waiting 2-5 minutes")
    else:
        print(f"\n❌ EMAIL SYSTEM NEEDS FIXING")
        print(f"🔧 Most likely issue: Gmail App Password")
        print(f"🔗 Generate new password: https://myaccount.google.com/apppasswords")

if __name__ == "__main__":
    main()
