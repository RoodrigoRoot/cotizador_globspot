from django.contrib import admin
from .models import Budget

# Register your models here.

class BudgeAdmin(admin.ModelAdmin):
    list_display = ["company", "company_contact", "updated_at"]
    


admin.site.register(Budget, BudgeAdmin)