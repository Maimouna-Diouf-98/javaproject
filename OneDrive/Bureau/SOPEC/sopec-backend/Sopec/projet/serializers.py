from rest_framework import serializers
from sites.serializers import SitesSerializer
from .models import Projet
from fichier_csv.serializers import ClientSerialiser
class ProjetSerializer(serializers.ModelSerializer):
    sites = SitesSerializer(many=True, read_only=True)
    client = ClientSerialiser(read_only=True) 

    class Meta:
        model = Projet
        fields = '__all__'
