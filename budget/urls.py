from django.urls import  path
from .views import IndexView, logout_view

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("salir/", logout_view, name="logout"),
]
