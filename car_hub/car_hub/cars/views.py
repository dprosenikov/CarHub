from django.contrib.auth.views import TemplateView
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')