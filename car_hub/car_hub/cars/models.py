from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count

from car_hub.cars.enums import CarBrands

UserModel = get_user_model()


class CarModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50, choices=[(b.name, b.value) for b in CarBrands])
    description = models.TextField(max_length=200)
    year = models.PositiveIntegerField()
    image = models.URLField(max_length=200)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f'{self.brand}, Year: {self.year},  Price: €{self.price}'


class CommentModel(models.Model):
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.TextField()


class LikeModel(models.Model):
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car.brand}, Year: {self.car.year},  Price: €{self.car.price} -> Liked By: {self.user}'
