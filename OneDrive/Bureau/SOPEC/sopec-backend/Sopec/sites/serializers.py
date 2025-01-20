from rest_framework import serializers

from fichier_csv.serializers import ClientSerialiser
from .models import Sites

class SitesSerializer(serializers.ModelSerializer):
    clients = ClientSerialiser(many=True, read_only=True)
    class Meta:
        model = Sites
        fields = '__all__' 
