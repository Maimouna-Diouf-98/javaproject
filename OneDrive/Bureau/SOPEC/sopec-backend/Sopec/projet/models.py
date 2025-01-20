
from django.db import models
from fichier_csv.models import Client
class Projet(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    nom = models.CharField(max_length=255) 
    adresse = models.CharField(max_length=255)  
    email = models.EmailField(max_length=255, unique=True)
    telephone = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom