from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from boards_app.models import Board
from .choices import status, priority


class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=250)
    status = models.CharField(choices=status)
    priority = models.CharField(choices=priority)
    assignee_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned")
    reviewer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviewer")
    due_date = models.DateField(default=timezone.now)


    def __str__(self):
        return self.title