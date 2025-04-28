from django.urls import path

from . import views

urlpatterns = [
    path('customer-register/',views.CustomerView.as_view(),name='customer-register'),
    path('customer-list/',views.CustomerListView.as_view(),name='customer-list'),
    path('customer-update/<uuid:uuid>/',views.CustomerUpdateView.as_view(), name='customer-update'),
    path('customer-delete/<uuid:uuid>/',views.CustomerDeleteView.as_view(), name='customer-delete'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-otp/', views.OTPVerificationView.as_view(), name='verify-otp'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    ]