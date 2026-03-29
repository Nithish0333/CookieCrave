#!/usr/bin/env python
"""Check if backend and frontend servers are running."""

import requests
import time

print("=" * 60)
print("CHECKING SERVER STATUS")
print("=" * 60)
print()

# Check backend
try:
    response = requests.get('http://localhost:8000/api/products/', timeout=2)
    if response.status_code == 200:
        print("✅ Backend Server: http://localhost:8000 - RUNNING")
    else:
        print(f"⚠️  Backend Server: http://localhost:8000 - Responding but status {response.status_code}")
except Exception as e:
    print(f"❌ Backend Server: http://localhost:8000 - NOT RUNNING ({str(e)[:50]})")

# Check frontend
for port in [5173, 5174]:
    try:
        response = requests.get(f'http://localhost:{port}/', timeout=2)
        if response.status_code == 200:
            print(f"✅ Frontend Server: http://localhost:{port} - RUNNING")
            break
    except:
        pass
else:
    print(f"❌ Frontend Server: http://localhost:5173 or 5174 - NOT RUNNING")

print()
print("=" * 60)
print("NEXT STEPS:")
print("1. If backend not running: cd backend && python manage.py runserver 0.0.0.0:8000")
print("2. If frontend not running: cd frontend && npm run dev")
print("3. Then refresh browser at http://localhost:5174 (hard refresh: Ctrl+Shift+R)")
print("=" * 60)
