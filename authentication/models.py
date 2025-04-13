from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class RoleChoices(models.TextChoices):

    ADMIN = 'Admin', 'Admin'

    VET = 'Vet', 'Vet'

    CUSTOMER = 'Customer', 'Customer'

    # SALES = 'Sales', 'Sales'

    # PET_TRAINER = 'Pet Trainer', 'Pet Trainer'

class Profile(AbstractUser):

    role = models.CharField(max_length=30,choices=RoleChoices.choices)

    def __str__(self):

        return f'{self.username}-{self.role}'
    
    class Meta:

        verbose_name = 'Profile'

        verbose_name_plural = 'Profile'


