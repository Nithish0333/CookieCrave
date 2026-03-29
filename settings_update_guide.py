
# FIND THIS LINE IN backend/core/settings.py:
EMAIL_HOST_PASSWORD = 'gkob nexx fykt imdd'

# REPLACE WITH YOUR NEW 16-CHARACTER APP PASSWORD:
EMAIL_HOST_PASSWORD = 'abcd efgh ijkl mnop'

# MAKE SURE THE REST OF THE EMAIL CONFIG IS CORRECT:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'cookiecrave001@gmail.com'
DEFAULT_FROM_EMAIL = 'cookiecrave001@gmail.com'
EMAIL_SUBJECT_PREFIX = '[CookieCrave] '
EMAIL_TIMEOUT = 30
    