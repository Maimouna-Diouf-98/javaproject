from django.urls import path
from projet.views import ProjetCreateAPI,ProjetDetail

urlpatterns = [
  path('create_projet', ProjetCreateAPI.as_view()),
  path('<int:pk>/', ProjetDetail.as_view()),
]
