from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from car_hub.profiles.managers import CarHubUserManager


class CarHubUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CarHubUserManager()


class Profile(models.Model):
    imageUrl = models.URLField(max_length=200)
    user = models.OneToOneField(CarHubUser, on_delete=models.CASCADE, primary_key=True)


from .signals import *
