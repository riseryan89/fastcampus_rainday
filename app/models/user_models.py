from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    locations = models.ManyToManyField("Location", related_name="user_location")

    def __str__(self):
        return self.username
