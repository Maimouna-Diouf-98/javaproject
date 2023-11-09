from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(requests):
    return render(requests, 'blog/blog_index.html')

def article(requests,numero_article):
     if numero_article in[1,2,3]:
        return render(requests, f"blog/article{numero_article}.html")
     else:
        return render(requests, f"blog/article_not_found.html")
