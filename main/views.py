from django.http import HttpResponse
from django.shortcuts import render


menu = [{'title': "Регистрация", 'url_name': "register"},
        {'title': "Войти", 'url_name': "login"}
]
def index(request):
    data = {
        'title': "Главная страница",
        'menu': menu,
    }
    return render(request,'main/index.html', context=data)

def register(request):
    return HttpResponse("Это страница регистрации")

def login(request):
    return HttpResponse("Это страница авторизации")