from django.db import models

# Create your models here.

from pet_app . models import BaseClass

class Veterinarian(BaseClass):

    name = models.CharField(max_length=20)

    qualification = models.CharField(max_length=30)

    contact = models.CharField(max_length=15)

    id_card = models.ImageField(upload_to='veterinary/',null=True, blank=True)

    place = models.CharField(max_length=25)

    def __str__(self):

        return f'{self.name} {self.qualification}'
    
    class Meta:

        verbose_name = 'Veterinarian'

        verbose_name_plural = 'Veterinarian'

        ordering = ['id']