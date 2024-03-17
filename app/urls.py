from django.urls import path
from .views import index, price_category, categories, remove_from_cart, add_to_cart, view_cart

urlpatterns = [
    path('category/<slug:category_slug>/', categories, name='category'),
    path('', index, name='index'),
    path('price-range/<int:a>/<int:b>/', price_category, name='price_category'),
    path('cart/', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),

]
