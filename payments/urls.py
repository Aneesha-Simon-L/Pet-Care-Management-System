from django.urls import path

from . import views

urlpatterns =[
    path('pay/<uuid:uuid>/', views.RazorpayView.as_view(), name='razorpay'),
    path('verify/', views.PaymentVerify.as_view(), name='payment-verify'),
    path('details/<uuid:uuid>/', views.PaymentDetailView.as_view(), name='payment-details'),
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
]
