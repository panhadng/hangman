from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json

from game.models import *


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
            return redirect('index')
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
    last_game = 0 if Game.objects.all().last() == None else Game.objects.all().last().id
    if new == 1:
        game = Game.objects.create(
            last_level=level, user_id=request.user, id=last_game+1)
        game_session = GameLevel.objects.create(
            game_id=game, level=Level.objects.filter(level=level).first())

    # fetch the game and level data
    game = Game.objects.filter(
        last_level=level, user_id=request.user).last()
    game_level = Level.objects.filter(level=level).first()
    game_session = GameLevel.objects.filter(
        game_id=game, level=game_level).first()
    if not game_session:
        game_session = GameLevel.objects.create(
            game_id=game, level=Level.objects.filter(level=level).first())
    game_word = Word.objects.filter(id=game_level.word_id.id).first()
    game_hint = Hint.objects.filter(id=game_level.hint_id.id).first()
    game_char = decrypt(game_word.text, game_session.guessed_strings)

    return render(request, "game/game.html", {
        "level": game_level.level,
        "word": game_word.text,
        "char": game_char,
        "category": game_word.category,
        "hint": game_hint.text,
        "game_id": game.id,
        "life":  game.lives_left,
        "score": game.total_game_score,
        "guess": {
            "guessed": False, }
    })


def guess(request, game_id):

    # retreive the necessary game data
    game = Game.objects.filter(id=game_id).first()
    game_level = Level.objects.filter(level=game.last_level).first()
    game_session = GameLevel.objects.filter(
        game_id=game_id, level=game_level).first()
    game_word = Word.objects.filter(id=game_level.word_id.id).first()
    word = game_word.text.lower()

    # get the current game chars
    game_char, char_array = decrypt(
        game_word.text, game_session.guessed_strings, both=True)

    if request.method == "POST":

        # work on the guess
        data = json.loads(request.body)
        guess = data['guess'].lower()
        type = data['type'].lower()
        extra_points, stream_word = 0, []

        if (type == "letter" and guess in word):
            game.total_game_score += 20
            game_session.level_game_score += 20

            # add the guess to the guessed strings
            game_session.guessed_strings += guess + "."
            game.save(), game_session.save()
            is_correct = True

        elif (type == "word" and guess == word):

            for i in range(len(word)):
                if char_array[i] == " _":
                    stream_word.append(word[i])

            extra_points += 20*len(list(set(stream_word)))
            game.total_game_score += extra_points
            game_session.level_game_score += extra_points

            # add the guess to the guessed strings
            game_session.guessed_strings += guess + "."
            game.save(), game_session.save()
            is_correct = True

        else:
            game.total_game_score -= 20
            game.lives_left -= 1
            game_session.level_game_score -= 20
            game.save(), game_session.save()
            is_correct = False

        # repopulate the characters to be guessed
        game_char = decrypt(game_word.text, game_session.guessed_strings)
        if "_" not in game_char:
            game.last_level += 1
            game_session.win = True
            game.save()

        print(game_char)

        return JsonResponse({
            "game_char": game_char,
            "guessed": True,
            "correct": True if is_correct else False,
            "message": "Congratulations! Your guess is correct." if is_correct else "Sorry, your guess is incorrect. Please try again.",
        })

    return redirect('game', level=game_level.level, new=0)


def decrypt(word, strings, both=False):

    # generate decrypted guessed characters
    char_array = [" _"] * len(word)
    guessed_chars = [item for item in strings.split(".")]

    for char in guessed_chars:
        for i in range(len(word)):
            if word.lower() == char.lower():
                char_array = [letter for letter in word]

            elif word[i].lower() == char.lower():
                char_array[i] = char.upper()

    game_char = ""
    for char in char_array:
        game_char += " " + char

    if both:
        return game_char, char_array

    return game_char


# Performance Views
def leaderboard(request):
    sort_by = request.GET.get('rank-type', 'score')  # Default to sorting by score
    users=User.objects.all()
    leaderboard=[]
    for user in users:
        games = Game.objects.filter(user_id=user)
        user_data = {
        "username": user.username,  
        "best_score": max(game.total_game_score for game in games),
        "highest_level": max(game.last_level for game in games),
        "longest_streak": 0,  
        }
        leaderboard.append(user_data)
    if sort_by == 'score':
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x["best_score"], reverse=True)
    elif sort_by == 'level':
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x["highest_level"], reverse=True)
    else:
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x["best_score"], reverse=True)
    return render(request, "game/leaderboard.html", {"leaderboard": sorted_leaderboard})

def profile(request):
    games = Game.objects.filter(user_id=request.user)
    user = request.user.username

    # scores and levels
    all_scores, all_levels = [], []
    for game in games:
        score, level = game.total_game_score, game.last_level
        all_scores.append(score), all_levels.append(level)

    context = {
        "user": user,
        "best_score": max(all_scores),
        "highest_level": max(all_levels)
    }
    return render(request, "game/profile.html", {
        "profile": context
    })


def chart(request):
    return render(request, "game/chart.html")


# Social Views
def social(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()

    return render(request, "game/social.html", {
        "posts": posts,
        "comments": comments,
    })


def post(request):
    if request.method == "POST":
        post = Post(author=request.user, post=request.POST['post'])
        post.save()

    return redirect('social')


def like(request, post_id):
    if request.method == 'GET':
        try:
            like = Like.objects.filter(
                liker=request.user, post_id=Post.objects.filter(id=post_id).first())
            return JsonResponse(len(like), safe=False)
        except Like.DoesNotExist:
            return JsonResponse({"error": "Like item not found."}, status=404)

    elif request.method == "POST":
        like = Like(liker=request.user,
                    post_id=Post.objects.filter(id=post_id).first())
        like.save()

        # update post like count
        post = Post.objects.filter(id=post_id).first()
        if post:
            post.like_count += 1
            post.save()

    elif request.method == 'DELETE':
        like = Like.objects.filter(
            liker=request.user, post_id=Post.objects.filter(id=post_id).first())
        like.delete()
        # update post like count
        post = Post.objects.filter(id=post_id).first()
        if post:
            post.like_count -= 1
            post.save()

    else:
        return JsonResponse({"error": "GET, POST or DELETE request required."})

    return redirect('social')


def comment(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if request.method == "POST":
        data = json.loads(request.body)
        comment = Comment(
            post_id=post,
            comment=data['comment'],
            author=request.user,
        )
        comment.save()
        return redirect('social')

    return redirect('social')


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
                if not Level.objects.filter(word_id=word, hint_id=hint).first():
                    level = Level.objects.create(
                        word_id=word, hint_id=hint)

        # check the word_data
        print(json.dumps(word_data, indent=4))

    return redirect('index')
