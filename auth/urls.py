from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.signin, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.log_out, name="logout"),

]