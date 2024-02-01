from django.http import HttpResponse
from django.shortcuts import render


def login_user(request):
    return HttpResponse("Это страница авторизации")


def logout_user(request):
    return HttpResponse("Это страница Логаута")


