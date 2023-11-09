from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


def index(requests):
    date = datetime.today()
    return render(requests,'formdjango/form_index.html',context={'date':date})