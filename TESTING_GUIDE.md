# Project Testing Guide

This guide describes how to verify the functionality of the **CookieCrave** application.

## 1. Automated Testing (Backend)
Django has a built-in testing framework that can be used to run your tests.

### How to Run Tests
1. Navigate to the `backend/` directory.
2. Ensure your virtual environment is active.
3. Run the following command:
```powershell
python manage.py test
```
This will automatically find and run all `tests.py` files in your Django apps.

---

## 2. API Manual Testing
You can use tools like **Postman** or **Insomnia** to test the backend API endpoints.

### Key Endpoints to Test
- `POST /api/users/register/` - User registration.
- `POST /api/users/login/` - User login.
- `GET /api/products/` - Retrieve product list.
- `POST /api/orders/checkout/` - Order creation (requires Razorpay keys).
- `GET /api/chatbot/` - Chatbot interaction.

---

## 3. Frontend Functional Testing
When testing the frontend manually at `http://localhost:5173`, verify the following:

- **Authentication**: Can you log in and sign up?
- **Products**: Are product images loading correctly from the backend?
- **Cart**: Can products be added to the cart and seen in the checkout page?
- **Checkout**: Does the Razorpay payment window open? (Ensure test keys are used).
- **Responsive Design**: Does the website look good on mobile and desktop?

---

## 4. Troubleshooting
- **Database Errors**: Ensure PostgreSQL is running and your `.env` credentials are correct.
- **Image Issues**: If images are missing, ensure `media/` folder exists in `backend/` or re-run image download scripts if needed.
- **Razorpay**: Make sure your `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` are correctly configured in `.env`.
