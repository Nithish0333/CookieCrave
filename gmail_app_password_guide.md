
STEP 1: ENABLE 2-FACTOR AUTHENTICATION
1. Go to: https://myaccount.google.com/security
2. Find "2-Step Verification" 
3. Click "Turn on" if not already enabled
4. Follow the setup process

STEP 2: GENERATE APP PASSWORD
1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to your Google account if prompted
3. Under "Select app", choose "Mail"
4. Under "Select device", choose "Other (Custom name)"
5. Enter name: "CookieCrave Django"
6. Click "Generate"

STEP 3: COPY THE APP PASSWORD
1. A 16-character password will appear
2. Format will be like: "abcd efgh ijkl mnop" (with spaces)
3. Copy this password exactly

STEP 4: UPDATE SETTINGS.PY
1. Open: backend/core/settings.py
2. Find: EMAIL_HOST_PASSWORD = '...'
3. Replace with the new 16-character app password
4. Save the file

STEP 5: RESTART DJANGO SERVER
1. Stop the current Django server
2. Run: python manage.py runserver
3. Test forgot password again
    