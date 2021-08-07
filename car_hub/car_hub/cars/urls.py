from django.urls import path

from car_hub.cars.views import index

urlpatterns = [
    path('', index, name='index'),
]