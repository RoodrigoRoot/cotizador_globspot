from django.shortcuts import render, redirect,reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Budget 
from .forms import BudgetModelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .utils import get_quantity

#Create your views here.

class IndexView(LoginRequiredMixin, View):
    login_url = "/login/"
    
    def get(self, request, *args, **kwargs):
        budgets = Budget.objects.all().order_by("-created_at")
        form = BudgetModelForm()
        
        return render(request, 'budget/index.html', locals())


class BudgetCreateView(CreateView, LoginRequiredMixin):
    model = Budget
    template_name = 'budget/budget_form.html'
    success_url = reverse_lazy('index')
    form_class = BudgetModelForm
    

    def post(self, request, *args, **kwargs):
        quantity = 0
        form = BudgetModelForm(request.POST)

        
        if form.is_valid():
            quantity += int(request.POST.get("vehicles"))
            quantity += int(request.POST.get("trucks"))
            quantity += int(request.POST.get("pets"))
            quantity += int(request.POST.get("people"))
            quantity += int(request.POST.get("containers"))
            quantity += int(request.POST.get("motorcycles"))
            price, total = get_quantity(quantity)

            budget = Budget.objects.create(
                company=form.cleaned_data['company'],
                company_contact=form.cleaned_data["company_contact"],
                vehicles=form.cleaned_data["vehicles"],
                trucks=form.cleaned_data["trucks"],
                pets=form.cleaned_data["pets"],
                people=form.cleaned_data["people"],
                containers=form.cleaned_data["containers"],
                motorcycles=form.cleaned_data["motorcycles"],
                creator=request.user,
                quantity=quantity,
                unit_cost=price,
                total=total
            )
            json3 = {'pk': budget.pk}

        return JsonResponse(json3, safe=False)


class BudgetUpdateView(UpdateView, LoginRequiredMixin):
    model = Budget
    template_name = 'budget/update_budget.html'
    success_url = reverse_lazy('index')
    form_class = BudgetModelForm


    def post(self, request, *args, **kwargs):
        quantity = 0
        json3 = {}
        try:
            form = BudgetModelForm(request.POST)
            if form.is_valid():
                self.object = self.get_object()
                print(self.object.pk)
                #budget_upd = form.save(commit=False)
                
                quantity += int(request.POST.get("vehicles"))
                quantity += int(request.POST.get("trucks"))
                quantity += int(request.POST.get("pets"))
                quantity += int(request.POST.get("people"))
                quantity += int(request.POST.get("containers"))
                quantity += int(request.POST.get("motorcycles"))
                price, total = get_quantity(quantity)

                
                self.object.company_id=request.POST.get('company')
                self.object.company_contact=request.POST.get("company_contact")
                self.object.vehicles=request.POST.get("vehicles")
                self.object.trucks=request.POST.get("trucks")
                self.object.pets=request.POST.get("pets")
                self.object.people=request.POST.get("people")
                self.object.containers=request.POST.get("containers")
                self.object.motorcycles=request.POST.get("motorcycles")
                self.object.quantity=quantity
                self.object.unit_cost=price
                self.object.creator=request.user
                self.object.total=total

                self.object.save()
            
                json3 = {"pk":self.object.pk}

        except  Exception as e:
            print(e)
        return JsonResponse(json3, safe=False)


class BudgetDeleteView(DeleteView, LoginRequiredMixin):
    model = Budget
    template_name = 'budget/delete_budget.html'
    success_url = reverse_lazy('index')
    