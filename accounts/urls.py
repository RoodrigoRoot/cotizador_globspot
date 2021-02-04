from django.urls import path
from .views import LoginView, logout_view

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("salir/", logout_view, name="logout"),
]
