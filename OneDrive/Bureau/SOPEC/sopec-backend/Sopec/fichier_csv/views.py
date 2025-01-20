import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client, DonneesAnnuelles, DonneesMensuelles
from  projet.models import Projet
from .serializers import ImportSerialiser
from rest_framework.exceptions import NotFound
import re
from rest_framework.parsers import MultiPartParser, FormParser
class ImportExcelAPIView(APIView):
    serializer_class = ImportSerialiser
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            fichiers = request.FILES
            serializer = self.serializer_class(data=fichiers)

            if not serializer.is_valid():
                return Response({'status': False, 'message': 'Fichier invalide ou non envoyé'}, status=status.HTTP_400_BAD_REQUEST)

            fichier_excel = fichiers.get('file')

            df = pd.read_excel(fichier_excel, sheet_name=0, engine='openpyxl', header=None)

         
            nom_client = self.extract_value(df, 'Nom client')
            niveau_tension = self.extract_value(df, 'Niveau de tension')
            categorie_tarifaire = self.extract_value(df, 'Categorie tarifaire')

            if not all([nom_client, niveau_tension, categorie_tarifaire]):
                return Response(
                    {"erreur": "Champs requis manquants : Nom client, Niveau de tension, ou Catégorie tarifaire"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                projet = Projet.objects.get(nom=nom_client)
            except Projet.DoesNotExist:
                return Response(
                    {"erreur": f"Le projet avec le nom '{nom_client}' n'existe pas."},
                    status=status.HTTP_404_NOT_FOUND
                )
         
            client, created = Client.objects.get_or_create(
                nom=nom_client,
                defaults={
                    "niveau_tension": niveau_tension,
                    "categorie_tarifaire": categorie_tarifaire
                }
            )

            projet.client = client
            projet.save()
          
            resultats = []

          
            indices_annees = df[df[0].str.contains('Année', na=False)].index.tolist()

            if not indices_annees:
                return Response({"erreur": "Aucune ligne 'Année' trouvée dans le fichier"}, status=status.HTTP_400_BAD_REQUEST)

            indices_annees = [idx for idx in indices_annees if idx < df.shape[0]]

            for i, annee_idx in enumerate(indices_annees):
                annee = df.iloc[annee_idx, 1] if annee_idx < df.shape[0] else None
                if not annee:
                    continue

                mois_ligne_idx = annee_idx + 1
                if mois_ligne_idx >= df.shape[0]:
                    continue

                mois = df.iloc[mois_ligne_idx, 1:].values
                donnees_debut_idx = mois_ligne_idx + 1
                if donnees_debut_idx >= df.shape[0]:
                    continue

                donnees = df.iloc[donnees_debut_idx:, 1:].values
                if len(mois) != donnees.shape[1]:
                    continue

                for j, mois_nom in enumerate(mois):
                    if j >= donnees.shape[1]:
                        continue

                    donnees_mensuelles = {}
                    if isinstance(mois_nom, str):
                        mois_nom = mois_nom.strip()
                    else:
                        continue

                    try:
                        donnees_mensuelles["Puissance souscrite (kW)"] = float(donnees[0][j])
                        donnees_mensuelles["K1 (kWh)"] = float(donnees[1][j])
                        donnees_mensuelles["K2 (kWh)"] = float(donnees[2][j])
                        donnees_mensuelles["Ma"] = float(donnees[3][j])
                        donnees_mensuelles["Energie Réactive (kWh)"] = float(donnees[4][j])
                        donnees_mensuelles["Puissance max relevée (kWh)"] = float(donnees[5][j])
                        donnees_mensuelles["Nombre de jour facturé"] = float(donnees[6][j])
                    except ValueError:
                        continue

                    resultats.append({
                        "annee": annee,
                        "mois": mois_nom,
                        "donnees": donnees_mensuelles
                    })

            rapport = {
                "donnees_ajoutees": [],
                "donnees_ignorées": [],
                "donnees_existantes": [] 
            }

            for resultat in resultats:
                donnees_annuelles, created = DonneesAnnuelles.objects.get_or_create(
                    client=client, annee=resultat['annee']
                )

             
                donnees_existantes = DonneesMensuelles.objects.filter(
                    Annuelles=donnees_annuelles,
                    mois=resultat['mois']
                ).exists()

                if donnees_existantes:
                  
                    rapport["donnees_existantes"].append({
                        "annee": resultat['annee'],
                        "mois": resultat['mois'],
                        "message": "Les données pour cette année et ce mois existent déjà."
                    })
                    continue

                DonneesMensuelles.objects.create(
                    Annuelles=donnees_annuelles,
                    mois=resultat['mois'],
                    puissance_souscrite=resultat['donnees']['Puissance souscrite (kW)'],
                    k1=resultat['donnees']['K1 (kWh)'],
                    k2=resultat['donnees']['K2 (kWh)'],
                    ma=resultat['donnees']['Ma'],
                    energie_reactive=resultat['donnees']['Energie Réactive (kWh)'],
                    puissance_max_releve=resultat['donnees']['Puissance max relevée (kWh)'],
                    nombre_de_jours_facture=resultat['donnees']['Nombre de jour facturé']
                )

                rapport["donnees_ajoutees"].append({
                    "annee": resultat['annee'],
                    "mois": resultat['mois']
                })

          
            rapport_organise = {"donnees_ajoutees": {}, "donnees_ignorées": {}, "donnees_existantes": {}}

            
            for item in rapport["donnees_ajoutees"]:
                annee = item["annee"]
                mois = item["mois"]
                if annee not in rapport_organise["donnees_ajoutees"]:
                    rapport_organise["donnees_ajoutees"][annee] = []
                rapport_organise["donnees_ajoutees"][annee].append(mois)

       
            for item in rapport["donnees_ignorées"]:
                annee = item["annee"]
                mois = item["mois"]
                if annee not in rapport_organise["donnees_ignorées"]:
                    rapport_organise["donnees_ignorées"][annee] = []
                rapport_organise["donnees_ignorées"][annee].append(mois)

            for item in rapport["donnees_existantes"]:
                annee = item["annee"]
                mois = item["mois"]
                if annee not in rapport_organise["donnees_existantes"]:
                    rapport_organise["donnees_existantes"][annee] = []
                rapport_organise["donnees_existantes"][annee].append({"mois": mois, "message": item["message"]})

            return Response(
                {
                    'status': True,
                    "message": 'Importation terminée',
                    "rapport": rapport_organise,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response({"erreur": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def extract_value(self, df, cle):
        try:
            ligne = df[df[0].str.contains(re.escape(cle), na=False, case=False)]
            if not ligne.empty:
                return ligne.iloc[0, 1]
            return None
        except Exception:
            return None

class DonneesClientsAPIView(APIView):


    def get(self, request, *args, **kwargs):
        try:
           
            clients = Client.objects.all()
            resultats = []

            for client in clients:
           
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
                        "annee": donnees_annee.annee,
                        "donnees_mensuelles": [
                            {
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

                resultats.append(donnees_client)

            return Response({"clients": resultats}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Erreur : {str(e)}")
            return Response({"erreur": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClientDataAPIView(APIView):
    def get(self, request, client_id):
        try:
           
            client = Client.objects.get(id=client_id)

            donnees_annuelles = DonneesAnnuelles.objects.filter(client=client)
            resultat = []

            for donnees in donnees_annuelles:

                donnees_mensuelles = DonneesMensuelles.objects.filter(Annuelles=donnees)
                mensuelles = [
                    {
                        "mois": mensuelle.mois,
                        "puissance_souscrite": mensuelle.puissance_souscrite,
                        "k1": mensuelle.k1,
                        "k2": mensuelle.k2,
                        "ma": mensuelle.ma,
                        "energie_reactive": mensuelle.energie_reactive,
                        "puissance_max_releve": mensuelle.puissance_max_releve,
                        "nombre_de_jours_facture": mensuelle.nombre_de_jours_facture,
                    }
                    for mensuelle in donnees_mensuelles
                ]

                resultat.append({
                    "annee": donnees.annee,
                    "donnees_mensuelles": mensuelles,
                })

            return Response({
                "status": True,
                "nom": client.nom,
                "niveau_tension": client.niveau_tension,
                "categorie_tarifaire": client.categorie_tarifaire,
                "donnees": resultat
            }, status=status.HTTP_200_OK)

        except Client.DoesNotExist:
            return Response({
                "status": False,
                "message": f"Le client avec l'ID {client_id} n'existe pas."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": False,
                "message": f"Erreur lors de la récupération des données : {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)


class SupprimerDonneesMensuellesAPIView(APIView):
 
    def delete(self, request, id, *args, **kwargs):
        try:
          
            donnees_mensuelles = DonneesMensuelles.objects.get(id=id)
            donnees_mensuelles.delete()

            return Response({"message": "Donnée mensuelle supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except DonneesMensuelles.DoesNotExist:
            raise NotFound(detail="Donnée mensuelle non trouvée avec cet ID.")
        
class SupprimerDonneesAnnuellesAPIView(APIView):
  
    def delete(self, request, id, *args, **kwargs):
        try:
            donnees_annuelles = DonneesAnnuelles.objects.get(id=id)
            donnees_annuelles.delete()

            return Response({"message": "Donnée annuelle supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except DonneesAnnuelles.DoesNotExist:
            raise NotFound(detail="Donnée annuelle non trouvée avec cet ID.")
