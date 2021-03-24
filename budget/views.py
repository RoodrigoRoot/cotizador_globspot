from django.shortcuts import render, redirect,reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Budget, Prices
from .forms import BudgetModelForm, PricesModelForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, FileResponse
from .utils import get_quantity, PDFHelper, delete_files
from django.conf import settings
from django.views.generic.list import ListView
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
                foreing=form.cleaned_data["foreing"],
                creator=request.user.profile,
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


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        quantity = 0
        json3 = {}
        try:
            self.object = self.get_object()
            form = BudgetModelForm(request.POST, instance=self.object)
            if form.is_valid():
                
                budget_upd = form.save(commit=False)
                
                quantity += int(request.POST.get("vehicles"))
                quantity += int(request.POST.get("trucks"))
                quantity += int(request.POST.get("pets"))
                quantity += int(request.POST.get("people"))
                quantity += int(request.POST.get("containers"))
                quantity += int(request.POST.get("motorcycles"))
                price, total = get_quantity(quantity)

                budget_upd.quantity=quantity
                budget_upd.unit_cost=price
                budget_upd.creator=request.user.profile
                budget_upd.total=total

                budget_upd.save()
            
                json3 = {"pk":budget_upd.pk}

        except  Exception as e:
            json3 = {"error":"KO"}
        return JsonResponse(json3, safe=False)


class BudgetDeleteView(DeleteView, LoginRequiredMixin):
    model = Budget
    template_name = 'budget/delete_budget.html'
    success_url = reverse_lazy('index')


class PDFDowloadView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        try:
            budget = Budget.objects.get(id=self.kwargs.get("pk"))
            PDFHelper.create_pdf_budget(budget)
            file = open(str(settings.BASE_DIR)+"/budget/Cotizacion_.pdf", 'rb')
            response = FileResponse(file)
            delete_files(budget)
            return response
        except  Exception as e:
            print(e)


class PricesListView(ListView, LoginRequiredMixin):
    model = Prices


class PricesDeleteView(DeleteView, LoginRequiredMixin):
    model = Prices
    template_name = 'budget/delete_price.html'
    success_url = reverse_lazy('prices_list')
    form_class = PricesModelForm


class PricesUpdateView(UpdateView, LoginRequiredMixin):
    model = Prices
    template_name = 'budget/update_price.html'
    success_url = reverse_lazy('prices_list')
    form_class = PricesModelForm

    def post(self, request, *args, **kwargs):
        json3 = {}
        form = PricesModelForm(request.POST or None)
        if form.is_valid():
            price_upd = form.save(commit=False)
            price = form.cleaned_data.get("price")
            price_upd.price = price
            price_upd.save()
            json3 = {"pk":price_upd.pk}
        return JsonResponse(json3, safe=False)