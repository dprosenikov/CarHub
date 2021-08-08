from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from car_hub.profiles.managers import CarHubUserManager

user_img = 'https://lh3.googleusercontent.com/proxy/srsv7ttgYG8RW-2SOQLH3NfJrIj7EwaYMZmi9V1Zk4Ug5y5Aq3F2_S4azDIbTxE9cqhtlrtFtwsP2KOpLbjOL--Q2JpXzP1pLZ0-1tyH7pARkXhPv4reFJEQQLcHuhRDIeCQSg'


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
