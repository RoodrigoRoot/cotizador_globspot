from django.contrib import admin
from .models import Budget, Prices

# Register your models here.

class BudgeAdmin(admin.ModelAdmin):
    list_display = ["company", "company_contact", "updated_at"]
    


admin.site.register(Budget, BudgeAdmin)

class PricesAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    


admin.site.register(Prices, PricesAdmin)