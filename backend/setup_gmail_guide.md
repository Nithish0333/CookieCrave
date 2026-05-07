# Gmail Setup Guide for CookieCrave

## Problem
Email sending failed because Gmail requires an App Password instead of your regular password.

## Solution: Set Up Gmail App Password

### Step 1: Enable 2-Factor Authentication
1. Go to: https://myaccount.google.com/security
2. Find "2-Step Verification" and turn it ON
3. Follow the setup process

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select:
   - App: Mail (or "Other" if Mail not available)
   - Device: CookieCrave Backend
3. Click "Generate"
4. Copy the 16-character password (it will look like: xxxx xxxx xxxx xxxx)

### Step 3: Update .env File
Replace the placeholder values in your .env file:

```env
# BEFORE (placeholders)
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password

# AFTER (your actual credentials)
GMAIL_EMAIL=your-actual-gmail@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
```

### Step 4: Restart Backend
After updating .env, restart the Django server:
```bash
python manage.py runserver
```

## Why This Works
- Gmail no longer allows regular passwords for apps
- App Passwords are secure, 16-character codes
- Each app gets its own password
- You can revoke passwords if needed

## Testing
After setup, test email sending:
```python
from django.core.mail import send_mail
send_mail(
    'Test Subject',
    'Test message from CookieCrave',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

## Troubleshooting
- If still failing: Double-check the 16-character password (no spaces)
- Ensure 2FA is enabled on the Gmail account
- Make sure you're using the correct Gmail address
- Check firewall/antivirus isn't blocking port 587
