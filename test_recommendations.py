import os
import django
import sys

# Add the project directory to the sys.path
sys.path.append('c:\\Users\\ASUS\\Desktop\\project1\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from recommendation_system.views import RecommendationAPIView
from rest_framework.test import APIRequestFactory, force_authenticate
from products.models import Product, Category

def test_recommendations():
    User = get_user_model()
    user = User.objects.first() # Get the first user (likely the admin I created)
    
    if not user:
        print("No user found")
        return

    factory = APIRequestFactory()
    view = RecommendationAPIView.as_view()
    
    # Test with default settings
    request = factory.get('/api/recommendations/recommendations/')
    force_authenticate(request, user=user)
    
    try:
        response = view(request)
        print(f"Status Code: {response.status_code}")
        print(f"Response Data: {response.data}")
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recommendations()
