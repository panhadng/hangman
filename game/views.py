from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "game/index.html")


def login(request):
    return render(request, "game/login.html")


def register(request):
    return render(request, "game/register.html")


def menu(request):
    return render(request, "game/menu.html")
