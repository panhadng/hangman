from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
import json

from game.models import Word, Hint, Level, Game, User, GameLevel


#  Authentication Views
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "game/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "game/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm-password"]
        if password != confirmation:
            return render(request, "game/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password)
            user.save()
        except IntegrityError:
            return render(request, "game/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "game/register.html")


#  Main Menu Views
def index(request):
    return render(request, "game/index.html")


def menu(request):
    return render(request, "game/menu.html")


# Game Views
def game(request, level, new):
    # load last game or create a new game
    last_game = 0 if not Game.objects.all().last() else Game.objects.all().last().id
    if new == 1:
        game = Game.objects.create(
            last_level=level, user_id=request.user, id=last_game+1)
        game_session = GameLevel.objects.create(
            game_id=game.id, level=Level.objects.filter(level=level).first())

    if request.method == "GET":
        # fetch the game and level data
        game = Game.objects.filter(
            last_level=level, user_id=request.user).last()
        game_level = Level.objects.filter(level=level).first()
        game_session = GameLevel.objects.filter(
            game_id=game.id, level=game_level).first()
        game_word = Word.objects.filter(id=game_level.word_id).first()

        char_array = [" _"]*len(game_word.text)
        for char in game_session.guessed_strings:
            for i in range(0, len(game_word.text)):
                if game_word.text[i].lower() == char.lower():
                    char_array[i] = char.upper()

        game_char = ""
        for char in char_array:
            game_char += " "+char

        game_hint = Hint.objects.filter(id=game_level.hint_id).first()

    return render(request, "game/game.html", {
        "level": game_level.level,
        "word": game_word.text,
        "char": game_char,
        "category": game_word.category,
        "hint": game_hint.text,
        "game_id": game.id,
        "life":  game.lives_left,
        "score": game.total_game_score,
    })


def guess(request, game_id):
    if request.method == "POST":
        game = Game.objects.filter(id=game_id).first()
        game_level = Level.objects.filter(level=game.last_level).first()

        # work on the guess
        guess = request.POST['guess'].lower()
        type = request.POST['guess-type'].lower()
        game_session = GameLevel.objects.filter(
            game_id=game_id, level=game_level).first()

        # retrieve our target word to verify
        word = Word.objects.filter(id=game_level.word_id).first().text.lower()

        if (type == "letter" and guess in word) or (type == "word" and guess == word):
            game.total_game_score += 20
            game_session.level_game_score += 20
            
            # add the guess to the guessed strings
            game_session.guessed_strings += guess
            game.save(), game_session.save()
        else:
            game.total_game_score -= 20
            game.lives_left -= 1
            game_session.level_game_score -= 20
            game.save(), game_session.save()

        return redirect('game', level=game_level.level, new=0)
    
    return redirect('game')


# Performance Views
def leaderboard(request):
    return render(request, "game/leaderboard.html")

def profile(request):
    return render(request, "game/profile.html")

def chart(request):
    return render(request, "game/chart.html")


# Setup Views
def populate(request):
    import json
    data_path = "game/data/words.json"

    with open(data_path, 'r') as f:
        words_data = json.load(f)

        for word_data in words_data:
            # check word and create if not exists
            word, _word = Word.objects.get_or_create(
                text=word_data['word'], category=word_data['category'])

            # check hint and create if not exists
            hint, _hint = Hint.objects.get_or_create(text=word_data['hint'])

            # if not exists create level and only if both word and hint were created successfully
            if hint and word and hint.id != None and word.id != None:
                if not Level.objects.filter(word_id=word.id, hint_id=hint.id).first():
                    level = Level.objects.create(
                        word_id=word.id, hint_id=hint.id)

        # check the word_data
        print(json.dumps(word_data, indent=4))

    return redirect('index')
