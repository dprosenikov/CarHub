from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from car_hub.profiles.managers import CarHubUserManager

user_img = 'data:image/png;base64,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'


class CarHubUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CarHubUserManager()


class Profile(models.Model):
    imageUrl = models.URLField(max_length=200, default=user_img)
    user = models.OneToOneField(CarHubUser, on_delete=models.CASCADE, primary_key=True)


from .signals import *
