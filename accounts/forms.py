from .models import Company
from django import forms

class CompanyModelForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ("name", "description")