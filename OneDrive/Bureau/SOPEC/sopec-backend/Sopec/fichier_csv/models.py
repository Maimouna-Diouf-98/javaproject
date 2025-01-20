from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=255, blank=True, null=True)
    niveau_tension = models.CharField(max_length=50, blank=True, null=True)
    categorie_tarifaire = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom if self.nom else "Client sans nom"

class DonneesAnnuelles(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='factures')
    annee = models.PositiveIntegerField()
    def __str__(self):
        return f" Annuelle {self.annee} pour {self.client.nom}"
    
class DonneesMensuelles(models.Model):
    Annuelles= models.ForeignKey(DonneesAnnuelles, on_delete=models.CASCADE, related_name='donnees_mensuelles')  
    mois = models.CharField(max_length=100)
    puissance_souscrite = models.FloatField()
    k1 = models.FloatField(verbose_name="K1 (kWh)")
    k2 = models.FloatField(verbose_name="K2 (kWh)")
    ma = models.FloatField(verbose_name="Ma")
    energie_reactive = models.FloatField(verbose_name="Énergie Réactive (kWh)")
    puissance_max_releve = models.FloatField(verbose_name="Puissance Max Relevée (kWh)")
    nombre_de_jours_facture = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
     return f"les donnees mensuelles pour de la   {self.Annuelles.client.nom} pour le mois {self.mois} de l' {self.Annuelles.annee} "

