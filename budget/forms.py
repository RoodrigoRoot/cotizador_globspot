from .models import Budget, Prices
from django import forms
#from accounts.models import Company

class BudgetModelForm(forms.ModelForm):
    
    company_contact = forms.CharField(required=True, label="Contacto", widget=forms.TextInput(
            attrs={'class': 'form-control',
            }
    ))


    vehicles = forms.IntegerField(label="Vehículos", initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control'}
    ))
    
    trucks = forms.IntegerField(label="Vehículos", initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control'}
    ))
    
    trucks = forms.IntegerField(label="Camiones", initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control'}
    ))
    
    people = forms.IntegerField(label="Personas", initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control'}
    ))
    
    pets = forms.IntegerField(label="Mascota", initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control'}
    ))
    
    containers = forms.IntegerField(label="Contenedores", initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control'}
    ))
    
    motorcycles  = forms.IntegerField(label="Motocicletas", initial=0, widget=forms.NumberInput(
        attrs={'class': 'form-control'}
    ))

    class Meta:
        model = Budget
        fields = ("company", "company_contact", "vehicles", "containers", "motorcycles", "trucks", "people", "pets", "foreing")


class PricesModelForm(forms.ModelForm):

    class Meta:
        model = Prices
        fields = ("name", "price")