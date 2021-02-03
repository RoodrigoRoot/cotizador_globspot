from django.shortcuts import render, redirect,reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Budget 
from braces.views import JSONResponseMixin

# Create your views here.

class IndexView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    
    def get(self, request, *args, **kwargs):
        budgets = Budget.objects.all()
        return render(request, 'budget/index.html', locals())


