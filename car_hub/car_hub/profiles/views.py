from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, RedirectView

from car_hub.profiles.forms import LoginForm, RegisterForm


class LoginUserView(LoginView):
    template_name = 'profiles/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        return reverse('index')


class RegisterUserView(CreateView):
    form_class = RegisterForm
    template_name = 'profiles/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LogoutUserView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutUserView, self).get(request, *args, **kwargs)
