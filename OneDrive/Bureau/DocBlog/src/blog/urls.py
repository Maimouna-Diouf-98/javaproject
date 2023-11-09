from django.urls import path
from .views import index,article
urlpatterns = [
    path('', index, name='blog_index'),
    path('article-<int:numero_article>/', article, name='blog_article'),
 
    
]