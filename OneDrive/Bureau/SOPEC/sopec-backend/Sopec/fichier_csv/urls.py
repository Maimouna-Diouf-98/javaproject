from django.urls import path
from fichier_csv import views

urlpatterns = [
  path('create_clients/', views.ImportExcelAPIView.as_view()),
  path('clients/', views.DonneesClientsAPIView.as_view()),
  path('<int:client_id>/', views.ClientDataAPIView.as_view()),
  path('mois/<int:id>/', views.SupprimerDonneesMensuellesAPIView.as_view(), name='supprimer_donnees_mensuelles'),
  path('annee/<int:id>/', views.SupprimerDonneesAnnuellesAPIView.as_view(), name='supprimer_donnees_annuelles'),

 
]
