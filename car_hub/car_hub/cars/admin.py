from django.contrib import admin

from car_hub.cars.models import CommentModel, CarModel, LikeModel

admin.site.register(CarModel)
admin.site.register(CommentModel)
admin.site.register(LikeModel)
