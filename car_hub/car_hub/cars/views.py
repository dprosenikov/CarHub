from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from car_hub.cars.forms import CommentForm, CarCreateForm
from car_hub.cars.models import CarModel, LikeModel, CommentModel
from car_hub.profiles.models import Profile


def index(request):
    return render(request, 'index.html')


class CarsListView(ListView):
    model = CarModel
    template_name = 'cars/cars_list.html'
    context_object_name = 'cars'
    paginate_by = 4


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
    success_url = reverse_lazy('my cars')
    context_object_name = 'cars'

    def form_valid(self, form):
        car = form.save(commit=False)
        car.user = self.request.user
        car.save()
        return super().form_valid(form)


class CarEditView(LoginRequiredMixin, UpdateView):
    model = CarModel
    template_name = 'cars/car_edit.html'
    form_class = CarCreateForm

    def get_success_url(self):
        car_id = self.kwargs['pk']
        return reverse_lazy('car details', kwargs={'pk': car_id})


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = CarModel
    template_name = 'cars/car_delete.html'
    success_url = reverse_lazy('my cars')
    context_object_name = 'car'


def my_cars(request):
    my_cars = CarModel.objects.filter(user_id=request.user.id)
    paginator = Paginator(my_cars, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cars/my_cars.html', {'page_obj': page_obj})


# class MyCarsView(LoginRequiredMixin, ListView):
#     model = CarModel
#     template_name = 'cars/my_cars.html'
#     context_object_name = 'cars'
#     success_url = reverse_lazy('my cars')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         my_cars = CarModel.objects.filter(user_id=self.request.user.id)
#         context['my_cars'] = my_cars
#         return context


def search_brand(request):
    if request.method == 'POST':
        searched_by = request.POST['searched_by']
        cars = CarModel.objects.filter(brand__contains=searched_by)
        return render(request, 'cars/search_results.html', {'searched_by': searched_by, 'cars': cars})
    else:
        return render(request, 'cars/search_results.html')
