from django.shortcuts import render, redirect,reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Budget 
from .forms import BudgetModelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse

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
        form = BudgetModelForm(request.POST)
        if form.is_valid():
            budget = Budget.objects.create(
                company=form.cleaned_data['company'],
                company_contact=form.cleaned_data["company_contact"],
                vehicles=form.cleaned_data["vehicles"],
                trucks=form.cleaned_data["trucks"],
                pets=form.cleaned_data["pets"],
                people=form.cleaned_data["people"],
                containers=form.cleaned_data["containers"],
                creator=request.user
            )
            json3 = {'pk': budget.pk}
        return JsonResponse(json3, safe=False)

class BudgetUpdateView(UpdateView, LoginRequiredMixin):
    model = Budget
    template_name = 'budget/update_budget.html'
    success_url = reverse_lazy('index')
    form_class = BudgetModelForm

class BudgetDeleteView(DeleteView, LoginRequiredMixin):
    model = Budget
    template_name = 'budget/delete_budget.html'
    success_url = reverse_lazy('index')
    