from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
# Create your views here.

class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'budget/index.html', locals())

def logout_view(request):
    logout(request)
    return redirect('/')