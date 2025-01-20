from django.contrib import admin
from fichier_csv import models


admin.site.register(models.Client)
admin.site.register(models.DonneesAnnuelles)
admin.site.register(models.DonneesMensuelles)

