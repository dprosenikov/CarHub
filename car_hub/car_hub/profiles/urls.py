from django.urls import path

from car_hub.profiles.views import LoginUserView, RegisterUserView, LogoutUserView, ProfileDetailsView, \
    ProfilesListView, profile_delete

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login user'),
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('logout/', LogoutUserView.as_view(), name='logout user'),
    path('profile/', ProfileDetailsView.as_view(), name='profile'),
    path('delete/profile/<int:pk>', profile_delete, name='delete profile'),
    path('allprofiles/', ProfilesListView.as_view(), name='all profiles'),
]
