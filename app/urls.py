from django.urls import path
from .views import index, price_category, categories, remove_from_cart, add_to_cart, view_cart, product_detail, \
    silk_care_instruction, refund_and_return

urlpatterns = [
    path('category/<slug:category_slug>/', categories, name='category'),
    path('', index, name='index'),
    path('price-range/<int:a>/<int:b>/', price_category, name='price_category'),
    path('cart/', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('product/<str:product_code>/', product_detail, name='product_detail'),
    path('silk-disclosure-instruction/', silk_care_instruction, name='silk_care_instruction'),
    path('refund-and-return-policy/', refund_and_return, name='refund_and_return')
]
