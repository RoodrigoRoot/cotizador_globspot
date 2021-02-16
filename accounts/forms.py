from .models import Company
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CompanyModelForm(forms.ModelForm):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={
        'class':'form-control'
    }))

    executive = forms.CharField(label="Contacto", widget=forms.TextInput(attrs={
        'class':'form-control'
    }))



    description =  forms.CharField(label="Descripcíon", required=False, widget=forms.Textarea(attrs={
        'class':'form-control',
        'rows':3
    }))
    
    class Meta:
        model = Company
        fields = ("name", "description")


class LoguinForm(AuthenticationForm):
    
    username = forms.CharField(label="Nombre de Usuario",
     widget=forms.TextInput(attrs={'autofocus': True,
    'class': 'form-control'}))

    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )
