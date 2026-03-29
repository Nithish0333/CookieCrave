# Project Setup Guide

This guide will walk you through setting up the **CookieCrave** project on your local machine.

## Prerequisites
Before you begin, ensure you have the following installed:
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/)

---

## 1. Backend Setup
The backend is built with Django and Django Rest Framework.

### Step 1: Create a Virtual Environment
Navigate to the `backend/` directory and create a virtual environment:
```powershell
cd backend
python -m venv venv
```

### Step 2: Activate the Virtual Environment
```powershell
# Windows
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
A `.env` file is already provided in the `backend/` directory. Ensure the following configurations match your local setup:
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (PostgreSQL)
- `GMAIL_EMAIL` and `GMAIL_APP_PASSWORD` (for sending emails)
- API Keys for Razorpay, OpenAI, and Unsplash.

### Step 5: Database Migrations
Create the database tables:
```powershell
python manage.py migrate
```

### Step 6: Create a Superuser (Optional)
To access the Django admin panel:
```powershell
python manage.py createsuperuser
```

### Step 7: Run the Backend Server
```powershell
python manage.py runserver
```

---

## 2. Frontend Setup
The frontend is built with React and Vite.

### Step 1: Install Dependencies
Navigate to the `frontend/` directory and install the required npm packages:
```powershell
cd ../frontend
npm install
```

### Step 2: Run the Development Server
```powershell
npm run dev
```
The frontend will typically be available at `http://localhost:5173`.

---

## 3. Standard Credentials
- **Admin Panel**: `http://localhost:8000/admin/`
- **Database**: Default PostgreSQL credentials should be updated in `.env`.
