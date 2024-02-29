from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User


class Message(models.Model):
    message = models.TextField()
    date = models.DateTimeField(default=datetime.now())
