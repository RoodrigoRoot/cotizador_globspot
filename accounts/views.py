from django.shortcuts import render
from django.shortcuts import render, redirect,reverse
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("index"))

        form = AuthenticationForm()
        return render(request, 'login.html', locals())
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid(): 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                authenticate(user)
                login(request, user)
                return redirect(reverse('index'))
        return render(request, 'login.html', locals())

def logout_view(request):
    logout(request)
    return redirect('/login/')
