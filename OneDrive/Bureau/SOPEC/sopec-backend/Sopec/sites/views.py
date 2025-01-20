from .models import Sites
from django.http import Http404
from django.shortcuts import get_object_or_404
from projet.models import Projet
from sites.serializers import SitesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SitesApi(APIView):
    def get(self, request, format=None):
        sites = Sites.objects.all() 
        serializer = SitesSerializer(sites, many=True) 
        return Response(serializer.data) 

    def post(self, request, format=None):
        serializer = SitesSerializer(data=request.data) 
        if serializer.is_valid():  
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
class SitesDetail(APIView):

    def get(self, request, pk, format=None):
        sites = get_object_or_404(Sites, pk=pk) 
        serializer = SitesSerializer(sites)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sites = get_object_or_404(Sites, pk=pk) 
        serializer = SitesSerializer(sites, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sites = get_object_or_404(Sites, pk=pk) 
        sites.delete()
        return Response({"message": "sites supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
