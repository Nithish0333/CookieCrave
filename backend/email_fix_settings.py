
# ADD TO settings.py

# Email Configuration - Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'cookiecrave001@gmail.com'
EMAIL_HOST_PASSWORD = 'YOUR_16_CHAR_APP_PASSWORD'  # Replace with app password
DEFAULT_FROM_EMAIL = 'cookiecrave001@gmail.com'

# Additional settings
EMAIL_SUBJECT_PREFIX = '[CookieCrave] '
EMAIL_TIMEOUT = 30
EMAIL_FAIL_SILENTLY = False  # For debugging

# Frontend URL
FRONTEND_URL = 'http://localhost:5173'
    