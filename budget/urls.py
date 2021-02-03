from django.urls import  path
from .views import IndexView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(IndexView.as_view()), name="index"),

]
