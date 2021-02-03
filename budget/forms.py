from .models import Budget
from django import forms

class Budget(forms.ModelForm):

    class Meta:
        model = Budget
        fields = ("company", "company_contact", "vehicle", "trucks", "people")