from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email Address')
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []