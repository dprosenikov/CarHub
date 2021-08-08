from django.urls import path

from car_hub.cars.views import index, CarsListView, CarDetailsView, like_car, comment_car, CarCreateView, CarEditView, \
    CarDeleteView, search_brand, my_cars

urlpatterns = [
    path('', index, name='index'),
    path('allcars/', CarsListView.as_view(), name='car list'),
    path('details/<int:pk>', CarDetailsView.as_view(), name='car details'),
    path('like/<int:pk>', like_car, name='like car'),
    path('comment/<int:pk>', comment_car, name='comment car'),
    path('create/', CarCreateView.as_view(), name='create car'),
    path('edit/<int:pk>', CarEditView.as_view(), name='edit car'),
    path('delete/<int:pk>', CarDeleteView.as_view(), name='delete car'),
    path('mycars/', my_cars, name='my cars'),
    path('searchresult/', search_brand, name='search cars'),
]
