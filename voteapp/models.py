from django.db import models
from django.contrib.auth.models import User

from foodyapi import settings


class Poll(models.Model):
    question = models.CharField(max_length=500)
    poll_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="polls")
    date_created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.question


class Choice(models.Model):
    text = models.CharField(max_length=500)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="choices")

    def __str__(self):
        return self.text

class Vote(models.Model):
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="votes")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")

    class Meta:
        unique_together = ('poll', 'voter')
    

    def __str__(self):
        return f'{self.voter} votes for "{self.choice}"'