import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-4-f#yh=zi-z^l=y7#kbx%$00i79-b)qg=z$e_#bz92#9x2zu0f'
DEBUG = True
ALLOWED_HOSTS = ['*', 'exportable-helmetlike-rowen.ngrok-free.dev']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'users.apps.UsersConfig',
    'products.apps.ProductsConfig',
    'orders.apps.OrdersConfig',
    'payments.apps.PaymentsConfig',
    'analytics.apps.AnalyticsConfig',
    'recommendation_system.apps.RecommendationSystemConfig',
    'chatbot.apps.ChatbotConfig',
    'discounts.apps.DiscountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'project1_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'

AUTH_USER_MODEL = 'users.User'
CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.authentication.SilentJWTAuthentication',
    )
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email Configuration - Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Hardcoded for now - replace with env vars later
EMAIL_HOST_USER = 'cookiecrave001@gmail.com'
EMAIL_HOST_PASSWORD = 'gkob nexx fykt imdd'
DEFAULT_FROM_EMAIL = 'cookiecrave001@gmail.com'
FRONTEND_URL = 'http://localhost:5173'

# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_XXXXXXXXXXXXXXXXXXXXXXX')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# Unsplash API Configuration
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY', '')

# Additional email settings for better deliverability
EMAIL_SUBJECT_PREFIX = '[CookieCrave] '
EMAIL_TIMEOUT = 30

# Fast2SMS Configuration
FAST2SMS_API_KEY = os.getenv('FAST2SMS_API_KEY', 'JrhlMkeC4yXRijqSBZOsf2xznNwp98L0gKVo7cmdQtGAHuYETaJoLlAntuEaXD4ZiqmH0bGcFO9Vw5TS')
FAST2SMS_ENTITY_ID = os.getenv('FAST2SMS_ENTITY_ID', '')
FAST2SMS_TEMPLATE_ID = os.getenv('FAST2SMS_TEMPLATE_ID', '')
FAST2SMS_SENDER_ID = os.getenv('FAST2SMS_SENDER_ID', 'FSTSMS')  # Change to your approved 6-letter Sender ID
