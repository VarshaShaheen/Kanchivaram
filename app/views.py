from django.shortcuts import render
from .models import Category, Product


def index(request):
    categories = Category.objects.all()
    return render(request, 'app/index.html', {'categories': categories})
