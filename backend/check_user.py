#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User

def check_user_password():
    print("=== Checking User Password ===")
    
    try:
        user = User.objects.get(email='nithish123@gmail.com')
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is Active: {user.is_active}")
        print(f"Password Hash: {user.password[:60]}...")
        
        # Test different passwords
        passwords_to_test = [
            "password123",
            "newpassword123", 
            "newtestpass123",
            "testpass123"
        ]
        
        print("\n=== Testing Passwords ===")
        for pwd in passwords_to_test:
            result = user.check_password(pwd)
            print(f"Password '{pwd}': {'✅ VALID' if result else '❌ INVALID'}")
            
    except User.DoesNotExist:
        print("❌ User not found!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_user_password()
