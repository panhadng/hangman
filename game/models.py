from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

# this model contains information about each game
class Game(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
