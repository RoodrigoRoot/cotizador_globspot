from django.db import models
from accounts.models import Company
# Create your models here.

class Budget(models.Model):
    company = models.ForeignKey(Company, verbose_name="Compañia", on_delete=models.CASCADE)
    company_contact = models.CharField(verbose_name="Contacto", max_length=150)
    vehicles = models.IntegerField(verbose_name="Vehículos", null=True, blank=True, default=0)
    people = models.IntegerField(verbose_name="Personas", null=True, blank=True, default=0)
    trucks = models.IntegerField(verbose_name="Camiones", null=True, blank=True, default=0)
    containers = models.IntegerField(verbose_name="Camiones", null=True, blank=True, default=0)
    motorcycles = models.IntegerField(verbose_name="Camiones", null=True, blank=True, default=0)
    pets = models.IntegerField(verbose_name="Mascotas", null=True, blank=True, default=0)
    creator = models.ForeignKey("accounts.Profile", verbose_name="Autor", on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0)
    unit_cost = models.SmallIntegerField(default=0)
    total = models.IntegerField(verbose_name="Total", default=0)
    created_at = models.DateTimeField(verbose_name="Creación", auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Modificación", auto_now=True, auto_now_add=False)
    foreing = models.BooleanField(verbose_name="Foraneo")
    
    def __str__(self):
        return self.company_contact
    
    
    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"

class Prices(models.Model):

    name = models.CharField(verbose_name="Rango", max_length=50)
    price = models.SmallIntegerField(default=0)
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name
    
