from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Company(models.Model):

    name = models.CharField(verbose_name="Compañia", max_length=150)
    description = models.TextField(verbose_name="Descripción", blank=True, null=True)
    executive = models.CharField(verbose_name="Ejecutivo", max_length=150)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

class Profile(models.Model):

    user = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
    charge = models.CharField(max_length=150, verbose_name="Cargo")

    def __str__(self):
        return self.user.username
