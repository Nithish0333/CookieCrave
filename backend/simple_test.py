#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def test_login_directly():
    print("=== Direct Login Test ===")
    
    try:
        # Get user
        user = User.objects.get(username='nithish')
        print(f"✅ Found user: {user.username}")
        print(f"✅ Email: {user.email}")
        print(f"✅ Is active: {user.is_active}")
        
        # Test password
        test_password = "newtestpass123"
        if user.check_password(test_password):
            print(f"✅ Password '{test_password}' is VALID")
        else:
            print(f"❌ Password '{test_password}' is INVALID")
            return
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        print(f"✅ Access Token: {str(access)[:50]}...")
        print(f"✅ Refresh Token: {str(refresh)[:50]}...")
        print("✅ Direct login test PASSED")
        
        return {
            'access': str(access),
            'refresh': str(refresh),
            'username': user.username
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    result = test_login_directly()
    if result:
        print("\n=== Use These Credentials for Frontend Test ===")
        print(f"Username: {result['username']}")
        print(f"Password: newtestpass123")
        print(f"Access Token: {result['access']}")
    else:
        print("❌ Direct login test FAILED")
