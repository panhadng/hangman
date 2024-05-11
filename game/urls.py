from django.urls import path

from . import views


urlpatterns = [

    path('', views.index, name="index"),

    # API Routes
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('menu', views.menu, name="menu"),

<<<<<<< HEAD
    path('leaderboard', views.leaderboard, name="leaderboard"),
=======
    # Performance Routes
    path('leaderboard', views.leaderboard, name="leaderboard"),
    path('profile', views.profile, name="profile"),
>>>>>>> design

    # Setup Routes
    path('populate', views.populate, name="populate"),

    # Game Routes
    path('game/level=<int:level>/new=<int:new>', views.game, name="game"),
    path('guess/game_id=<int:game_id>', views.guess, name="guess"),

]
