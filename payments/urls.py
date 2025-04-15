from django.urls import path

from . import views

urlpatterns =[
    path('pet-payment-details/',views.PetPaymentView.as_view(),name='pet-payment-details'),

    path('razorpay-view/',views.RazorPayView.as_view(),name='razorpay-view'),

    path('payment-verify/',views.PaymentVerifyView.as_view(),name='payment-verify')
]