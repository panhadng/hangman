from django.shortcuts import render


#  All the views
def index(request):
    return render(request, "game/index.html")


def login(request):
    return render(request, "game/login.html")


def register(request):
    return render(request, "game/register.html")


def menu(request):
    return render(request, "game/menu.html")


def game(request):
    return render(request, "game/game.html")
