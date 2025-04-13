from django.urls import path

from . import views

urlpatterns = [
    path('customer-register/',views.CustomerView.as_view(),name='customer-register'),]