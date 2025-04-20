from django.db import models

# Create your models here.

import uuid

# Create your models here.

class BaseClass(models.Model):

    uuid = models.SlugField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True 

class PetCategoryChoices(models.TextChoices):

    DOG = 'DOG', 'DOG'

    CAT = 'CAT', 'CAT'

    BIRD = 'BIRD', 'BIRD'

    REPTILE = 'REPTILE', 'REPTILE'

    FISH = 'FISH', 'FISH'

    OTHER = 'OTHER', 'OTHER'
 
class PetGenderChoices(models.TextChoices):

    MALE = 'MALE', 'MALE'

    FEMALE = 'FEMALE', 'FEMALE'

    UNKNOWN = 'UNKNOWN', 'UNKNOWN'

class PetStatusChoices(models.TextChoices):

    OWNED = 'OWNED', 'OWNED'

    FOSTER = 'FOSTER', 'FOSTER'

class AppointmentStatus(models.TextChoices):

    PENDING = 'PENDING', 'PENDING'

    SCHEDULED = 'SCHEDULED', 'SCHEDULED'

    APPROVED = 'APPROVED', 'APPROVED'

    REJECTED = 'REJECTED', 'REJECTED'

class PetServiceChoices(models.TextChoices):

    GROOMING = 'GROOMING', 'GROOMING'

    PET_SPA = 'PET SPA', 'PET SPA'

    TRAINING = 'TRAINING', 'TRAINING'

    PET_SITTING = 'PET SITTING', 'PET SITTING'

    VETERINARY = 'VETERINARY', 'VETERINARY'

    VACCINATION = 'VACCINATION', 'VACCINATION'

    PET_PHOTOGRAPHY = 'PET PHOTOGRAPHY', 'PET PHOTOGRAPHY'

class Pets(BaseClass):

    customer = models.ForeignKey('customer.Customer',on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50)

    category = models.CharField(max_length=20,choices=PetCategoryChoices.choices)

    breed = models.CharField(max_length=25, null=True, blank=True)

    age = models.IntegerField(null=True, blank=True)

    gender = models.CharField(max_length=10,choices=PetGenderChoices.choices)
    
    photo = models.ImageField(upload_to='pets/', null=True, blank=True)

    status = models.CharField(max_length=20,choices=PetStatusChoices.choices)

    registration_date = models.DateField(auto_now_add=True)

    adm_number = models.CharField(max_length=50,null=True, blank=True)

    last_vet_visit = models.DateField(null=True, blank=True)
    
    is_vaccinated = models.BooleanField(default=False)

    service_type = models.CharField(max_length=20,choices=PetServiceChoices.choices)

    appointment_date = models.DateField()

    appointment_status = models.CharField(max_length=50,choices=AppointmentStatus.choices,default='SCHEDULED')

    def __str__(self):

        return f'{self.name} ({self.category})'

    class Meta:

        verbose_name = 'pet'

        verbose_name_plural = 'Pets'

        ordering = ['id']
