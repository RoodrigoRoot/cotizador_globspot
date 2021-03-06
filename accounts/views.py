from django.shortcuts import render, redirect,reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Company
from .forms import  CompanyModelForm, LoguinForm
from django.http import JsonResponse
# Create your views here.

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("index"))

        form = LoguinForm()
        return render(request, 'login.html', locals())
    
    def post(self, request, *args, **kwargs):
        form = LoguinForm(data=request.POST)
        
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

class CompanyListView(ListView, LoginRequiredMixin):
    model = Company

class CompanyCreateView(CreateView, LoginRequiredMixin):
    model = Company
    template_name = 'accounts/company.html'
    success_url = reverse_lazy('companies')
    form_class = CompanyModelForm

    def post(self, request, *args, **kwargs):
        json3 = {}
        form = CompanyModelForm(request.POST)
        if form.is_valid():
            company = Company.objects.create(
                name=form.cleaned_data["name"],
                executive=form.cleaned_data["executive"],
                description=form.cleaned_data["description"]
            )
            if company:    
                json3 = {'pk': company.pk}

        return JsonResponse(json3)

class CompanyUpdateView(UpdateView, LoginRequiredMixin):
    model = Company
    template_name = 'accounts/update_company.html'
    success_url = reverse_lazy('companies')
    form_class = CompanyModelForm

    def post(self, request, *args, **kwargs):
        json3 = {}
        comp = Company.objects.get(id=self.kwargs["pk"])
        self.object = self.get_object()
        form = CompanyModelForm(request.POST, instance=self.object)
        if form.is_valid():
            comp.name = form.cleaned_data["name"]
            comp.description = form.cleaned_data["description"]
            comp.executive = form.cleaned_data["executive"]
            comp.save()
            json3 = {"pk":comp.id}
        return JsonResponse(json3, safe=False)


class CompanyDeleteView(DeleteView, LoginRequiredMixin):
    model = Company
    template_name = 'accounts/delete_company.html'
    success_url = reverse_lazy('companies')


def get_company_contact(request):

    executive = Company.objects.get(id=int(request.GET["comp_id"])).executive
    json3 = {'executive': executive}

    return JsonResponse(json3)

