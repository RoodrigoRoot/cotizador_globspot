from django.db import models
from django.contrib.auth.models import User
from accounts.models import Company
# Create your models here.

class Budget(models.Model):
    company = models.ForeignKey(Company, verbose_name="Compañia", on_delete=models.CASCADE)
    company_contact = models.CharField(verbose_name="Compañia", max_length=150)
    vehicles = models.IntegerField(verbose_name="Vehículos")
    people = models.IntegerField(verbose_name="Personas")
    truck = models.IntegerField(verbose_name="Camiones")
    pets = models.IntegerField(verbose_name="Mascotas")
    creator = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Creación", auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificación", auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.company
    
    def __repr__(self):
        return self.company
    
    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"



