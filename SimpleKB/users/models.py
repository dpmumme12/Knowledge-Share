from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField('profile_images', null=True, blank=True)
