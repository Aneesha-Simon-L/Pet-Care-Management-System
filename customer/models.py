from django.db import models

# Create your models here.

from pet_app.models import BaseClass

class Customer(BaseClass):

    profile = models.OneToOneField('authentication.Profile',on_delete=models.CASCADE)

    name = models.CharField(max_length=60)

    contact = models.CharField(max_length=15)

    email = models.EmailField(unique=True)

    place = models.CharField(max_length=25)

    def __str__(self):

        return f'{self.name}'
    
    class Meta:

        verbose_name = 'Customer'

        verbose_name_plural = 'Customers'

        ordering = ['id']
