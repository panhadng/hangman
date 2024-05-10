from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.index, name="index"),

    # API routes
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('menu', views.menu, name="menu"),
    path('game', views.game, name="game"),
    path('leaderboard', views.leaderboard, name="leaderboard"),
    path('profile', views.profile, name="profile"),

]
