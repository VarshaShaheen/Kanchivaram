from django.urls import path
from .views import index, price_category

urlpatterns = [
    path('', index, name='index'),
    path('price-range/<int:a>/<int:b>/', price_category, name='price_category'),
]