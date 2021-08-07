from django.urls import path

from car_hub.profiles.views import LoginUserView, RegisterUserView, LogoutUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login user'),
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('logout/', LogoutUserView.as_view(), name='logout user'),
]
