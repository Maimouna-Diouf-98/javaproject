from django.db import models
from projet.models import Projet

class Sites(models.Model):
    nom = models.TextField(max_length=255)
    adresse = models.CharField(max_length=255)  
    consomation = models.CharField(max_length=255)
    tension = models.CharField(max_length=255)
    category= models.CharField(max_length=255)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='sites') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom