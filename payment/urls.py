from django.urls import path

from .views import *

urlpatterns = [
    path('', PaymentView.as_view(), name='checkout'),
    path('verify/', payment_verification, name='verify'),
]
