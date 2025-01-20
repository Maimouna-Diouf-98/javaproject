from django.http import Http404
from django.shortcuts import get_object_or_404
from projet.models import Projet
from fichier_csv.models import DonneesAnnuelles,DonneesMensuelles,Client
from projet.serializers import ProjetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProjetCreateAPI(APIView):
   
    def get(self, request, format=None):
        projets = Projet.objects.all() 
        serializer = ProjetSerializer(projets, many=True)
        return Response(serializer.data) 

   
    def post(self, request, format=None):
        serializer = ProjetSerializer(data=request.data)  
        if serializer.is_valid():  
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ProjetDetail(APIView):
    def get(self, request, pk):
        try:
            
            projet = Projet.objects.get(id=pk)

          
            client = projet.client

            
            donnees_annuelles = DonneesAnnuelles.objects.filter(client=client)
            donnees_client = {
                "id": client.id,
                "nom": client.nom,
                "niveau_tension": client.niveau_tension,
                "categorie_tarifaire": client.categorie_tarifaire,
                "donnees_annuelles": [],
            }

         
            for donnees_annee in donnees_annuelles:
                donnees_mensuelles = DonneesMensuelles.objects.filter(Annuelles=donnees_annee)
                donnees_annee_data = {
                    "id":donnees_annee.id,
                    "annee": donnees_annee.annee,
                    "donnees_mensuelles": [
                        {   
                            "id":donnee.id,
                            "mois": donnee.mois,
                            "puissance_souscrite": donnee.puissance_souscrite,
                            "k1": donnee.k1,
                            "k2": donnee.k2,
                            "ma": donnee.ma,
                            "energie_reactive": donnee.energie_reactive,
                            "puissance_max_releve": donnee.puissance_max_releve,
                            "nombre_de_jours_facture": donnee.nombre_de_jours_facture,
                        }
                        for donnee in donnees_mensuelles
                    ],
                }
                donnees_client["donnees_annuelles"].append(donnees_annee_data)

            return Response({
                "projet": {
                    "id": projet.id,
                    "nom": projet.nom,
                    "adresse":projet.adresse,
                    "email":projet.email,
                    "telephone ":projet.telephone,
                    "client": donnees_client
                }
            }, status=status.HTTP_200_OK)

        except Projet.DoesNotExist:
            return Response({"erreur": "Projet non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"erreur": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk, format=None):
        projet = get_object_or_404(Projet, pk=pk) 
        serializer = ProjetSerializer(projet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        projet = get_object_or_404(Projet, pk=pk)  
        projet.delete()
        return Response({"message": "Projet supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
