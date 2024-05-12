from django.db import models
from django.contrib.auth.models import AbstractUser


# user authentication
class User(AbstractUser):
    pass


# gamification
class Badge(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    requirement = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Badge {self.name} with an ID of {self.id}"


# user profile
class Profile(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    badge_id = models.ForeignKey("Badge", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id}"


# in-game mechanics
class Word(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Word ID of {self.id}: {self.text} in {self.category} category."


class Hint(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    text = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Hint ID of {self.id}: {self.text}"


class Level(models.Model):
    level = models.IntegerField(primary_key=True, auto_created=True)
    word_id = models.ForeignKey("Word", on_delete=models.CASCADE)
    hint_id = models.ForeignKey("Hint", on_delete=models.CASCADE)

    def __str__(self):
        return f"Level {self.level}: Word ID of {self.word_id} and Hint ID of {self.hint_id}."


# levelling
class Game(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, default=1)
    total_game_score = models.IntegerField(default=100)
    last_level = models.IntegerField(default=1)
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    lives_left = models.IntegerField(default=20)

    def __str__(self):
        return f"Game ID of {self.id}: Last Level of {self.last_level} with {self.lives_left} Lives Left."


class GameLevel(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    level = models.ForeignKey("Level", on_delete=models.CASCADE)
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    level_game_score = models.IntegerField(default=100)
    guessed_strings = models.CharField(
        max_length=25, default=" .", null=True, blank=True)
    win = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.level} Only '{self.guessed_strings}' guessed."


# playing
TYPES = [("Letter", "Word")]


class Guess(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    type = models.CharField(max_length=50, choices=TYPES, blank=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    game_level_id = models.ForeignKey("GameLevel", on_delete=models.CASCADE)
    guess_datetime = models.DateTimeField(auto_now_add=True)
    result = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Guess of {self.text} made on {self.guess_datetime}"


# social hub
class Post(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    post = models.TextField()
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post written by {self.author} at {self.timestamp}"


class Like(models.Model):
    liker = models.ForeignKey("User", on_delete=models.CASCADE)
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.liker} likes {self.post_id}"


class Comment(models.Model):
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment of {self.post_id} written by {self.author} at {self.timestamp}"
