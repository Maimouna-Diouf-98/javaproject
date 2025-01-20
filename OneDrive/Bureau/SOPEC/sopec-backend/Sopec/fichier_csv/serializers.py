from rest_framework import serializers
from .models import Client, DonneesMensuelles,DonneesAnnuelles



class ClientSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = [ 'nom', 'niveau_tension', 'categorie_tarifaire']
        extra_kwargs = {
            'nom': {'required': False},
            'niveau_tension': {'required': False},
            'categorie_tarifaire': {'required': False},
        }

class DonneesAnnuellesSerializer(serializers.ModelSerializer):
    client = ClientSerialiser(many=True, read_only=True)
    class Meta:
        model = DonneesAnnuelles
        fields = '__all__'

class DonneesMensuellesSerializer(serializers.ModelSerializer):
    annuelles = DonneesAnnuellesSerializer(many=True, read_only=True)
    class Meta:
        model = DonneesMensuelles
        fields = '__all__'
        
class ImportSerialiser(serializers.Serializer):
    file=serializers.FileField()
    class Meta:
    
        fields = ['file']
