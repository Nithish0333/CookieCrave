
# UPDATED EMAIL CONFIGURATION
# Add these to your settings.py

# Email Configuration - Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'cookiecrave001@gmail.com'
EMAIL_HOST_PASSWORD = 'YOUR_16_CHARACTER_APP_PASSWORD'  # Replace with app password
DEFAULT_FROM_EMAIL = 'cookiecrave001@gmail.com'

# Additional settings for better deliverability
EMAIL_SUBJECT_PREFIX = '[CookieCrave] '
EMAIL_TIMEOUT = 30
EMAIL_FAIL_SILENTLY = False  # Set to False for debugging

# Frontend URL for password reset links
FRONTEND_URL = 'http://localhost:5173'
    