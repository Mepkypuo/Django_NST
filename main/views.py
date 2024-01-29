from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse('Это главная страница приложения NST.')
