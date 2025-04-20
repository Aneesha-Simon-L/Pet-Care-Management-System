from django.urls import path

from . import views

from . views import update_pet_status

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('about/',views.AboutusView.as_view(),name='about'),
    path('contact/',views.ContactusView.as_view(),name='contact'),
    path('contact-success/',views.ContactSuccessView.as_view(),name='contact-success'),
    path('service/',views.ServiceView.as_view(),name='service'),
# Pet related URLs
    path('service-register/',views.PetRegistrationView.as_view(), name='service-register'),
    path('pet-list/',views.PetListView.as_view(),name='pet-list'),
    path('thank-you/<str:uuid>/',views.ThankYouView.as_view(), name='thank-you'),
    path('pet-update/<uuid:uuid>/',views.PetUpdateView.as_view(), name='pet-update'),
    path('pet-delete/<uuid:uuid>/',views.PetDeleteView.as_view(), name='pet-delete'),
    path('pet/<str:uuid>/update-status/', update_pet_status, name='update-status'),
]
