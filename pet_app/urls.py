from django.urls import path

from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('about/',views.AboutusView.as_view(),name='about'),
    path('contact/',views.ContactusView.as_view(),name='contact'),
    path('service/',views.ServiceView.as_view(),name='service'),
# Pet related URLs
    path('service-register/',views.PetRegistrationView.as_view(), name='service-register'),
    path('pet-list/',views.PetListView.as_view(),name='pet-list'),
    path('thank-you/<int:pet_id>/',views.ThankYouView.as_view(), name='thank-you'),
    # path('pets/<int:pk>/',views.PetDetailView.as_view(), name='pet-detail'),
    # path('pets/',views.PetListView.as_view(), name='pet-list'),
]
