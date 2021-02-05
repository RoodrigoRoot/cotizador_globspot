from django.db import models

# Create your models here.

class Company(models.Model):

    name = models.CharField(verbose_name="Compañia", max_length=150)
    description = models.TextField(verbose_name="Descripción", blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
