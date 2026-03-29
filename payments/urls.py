from django.urls import path
from . import views

urlpatterns = [
    # Razorpay payment endpoints
    path('razorpay/create-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('razorpay/verify-payment/', views.verify_payment, name='verify_payment'),
    path('razorpay/verify-wholesale/', views.verify_wholesale_payment, name='verify_wholesale_payment'),
    # Order management
    path('create-order/', views.create_order, name='create_order'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<str:order_id>/', views.order_detail, name='order_detail'),
]
