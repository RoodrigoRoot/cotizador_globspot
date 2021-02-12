from django.shortcuts import render, redirect,reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Budget 
from .forms import BudgetModelForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, FileResponse
from .utils import get_quantity, PDFHelper
from django.conf import settings

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
                budget_upd.creator=request.user
                budget_upd.total=total

                budget_upd.save()
            
                json3 = {"pk":budget_upd.pk}

        except  Exception as e:
            json3 = {"error":"KO"}
            print(e)
        return JsonResponse(json3, safe=False)


class BudgetDeleteView(DeleteView, LoginRequiredMixin):
    model = Budget
    template_name = 'budget/delete_budget.html'
    success_url = reverse_lazy('index')


class PDFDowloadView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        try:
            budget = Budget.objects.get(id=self.kwargs.get("pk"))
            print(budget)
            PDFHelper.create_pdf_budget(budget)
            file = open(str(settings.BASE_DIR)+"/budget/Cotizacion.pdf", 'rb')
            #import os
            #os.remove(str(settings.BASE_DIR)+"/budget/Cotizacion.pdf")
            #response = HttpResponse("file", content_type='application/force-download', charset="utf-8")
            #response['Content-Disposition'] = 'attachment; filename="{}"'.format(uni_filename)
            response = FileResponse(file)
            return response
        except  Exception as e:
            print(e)




