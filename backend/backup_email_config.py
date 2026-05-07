
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
    