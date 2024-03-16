from django.shortcuts import render
from .models import Category, Product


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'app/index.html', {'categories': categories, 'products': products})


def price_category(request, a, b):
    products_in_range = Product.objects.filter(mrp__gte=a, mrp__lte=b)
    return render(request,'app/price_category/price_category.html', {'products': products_in_range})