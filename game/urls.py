from django.urls import path
from django.http import HttpResponse

from . import views


def no_favicon(request):
    return HttpResponse(status=204)


urlpatterns = [
    # defaults
    path('favicon.ico', no_favicon),
    path('', views.index, name="index"),

    # API Routes
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('menu', views.menu, name="menu"),

    # Performance Routes
    path('leaderboard', views.leaderboard, name="leaderboard"),
    path('profile', views.profile, name="profile"),

    # Setup Routes
    path('populate', views.populate, name="populate"),

    # Game Routes
    path('game/level=<int:level>/new=<int:new>', views.game, name="game"),
    path('guess/game_id=<int:game_id>', views.guess, name="guess"),

]
