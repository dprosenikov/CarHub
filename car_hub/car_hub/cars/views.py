from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, RedirectView, CreateView

from car_hub.cars.forms import CommentForm, CarCreateForm
from car_hub.cars.models import CarModel, LikeModel, CommentModel


def index(request):
    return render(request, 'index.html')


class CarsListView(ListView):
    model = CarModel
    template_name = 'cars/cars_list.html'
    context_object_name = 'cars'


class CarDetailsView(DetailView):
    model = CarModel
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = context['car']
        car.likes_count = car.likemodel_set.count()
        is_owner = car.user == self.request.user
        is_liked = car.likemodel_set.filter(user_id=self.request.user.id).first()
        context['comment'] = CommentForm()
        context['comments'] = car.commentmodel_set.all()
        context['is_owner'] = is_owner
        context['is_liked'] = is_liked
        return context


def like_car(request, pk):
    car = CarModel.objects.get(pk=pk)
    is_liked = car.likemodel_set.filter(user_id=request.user.id).first()
    if is_liked:
        is_liked.delete()
    else:
        like = LikeModel(car=car, user=request.user)
        like.save()
    return redirect('car details', pk)


def comment_car(request, pk):
    car = CarModel.objects.get(pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = CommentModel(comment=form.cleaned_data['comment'], car=car, user=request.user)
        comment.save()
    return redirect('car details', car.id)


class CarCreateView(LoginRequiredMixin, CreateView):
    template_name = 'cars/car_create.html'
    model = CarModel
    form_class = CarCreateForm
    success_url = reverse_lazy('car list')
    context_object_name = 'cars'

    def form_valid(self, form):
        car = form.save(commit=False)
        car.user = self.request.user
        car.save()
        return super().form_valid(form)
