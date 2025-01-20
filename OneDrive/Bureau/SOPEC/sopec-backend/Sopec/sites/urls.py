from django.urls import path
from sites import views

urlpatterns = [
  path('create_site', views.SitesApi.as_view()),
  path('<int:pk>/', views.SitesDetail.as_view()),
 
]
