from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=25)
    members = models.ManyToManyField(User, related_name="member_of_boards")
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="board_owner")


    def __str__(self):
        return self.title