from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, RedirectView, FormView, DeleteView, ListView

from car_hub.cars.models import CarModel
from car_hub.profiles.forms import LoginForm, RegisterForm, ProfileForm
from car_hub.profiles.models import Profile, CarHubUser


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


class ProfileDetailsView(LoginRequiredMixin, FormView):
    template_name = 'profiles/user_profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.request.user.id)
        profile.imageUrl = form.cleaned_data['imageUrl']
        profile.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.request.user.id)
        return context


# class ProfileDeleteView(LoginRequiredMixin, DeleteView):
#     model = Profile
#     template_name = 'profiles/profile_delete.html'
#     context_object_name = 'prof'
#
#     def get_success_url(self):
#         carhub_user = CarHubUser.objects.get(id=self.request.user.id)
#         carhub_user.delete()
#         return reverse('index')


def profile_delete(request, pk):
    profile = Profile.objects.get(user_id=pk)
    if request.method == 'POST':
        carhub_user = CarHubUser.objects.get(id=pk)
        carhub_user.delete()
        profile.delete()
        if (request.user.is_superuser and pk == request.user.id) or not request.user.is_superuser:
            logout(request)
            return redirect('index')
        else:
            return redirect('all profiles')
    else:
        return render(request, 'profiles/profile_delete.html', {'profile': profile})


class ProfilesListView(ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'
    context_object_name = 'profiles'
