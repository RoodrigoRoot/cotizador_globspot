from .models import Company
from django import forms

class CompanyModelForm(forms.ModelForm):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={
        'class':'form-control'
    }))

    
    description =  forms.CharField(label="Descripcíon", required=False, widget=forms.Textarea(attrs={
        'class':'form-control',
        'rows':3
    }))
    class Meta:
        model = Company
        fields = ("name", "description")