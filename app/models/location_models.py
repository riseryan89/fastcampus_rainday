from django.db import models

from app.models import User


class Location(models.Model):
    location = models.CharField(max_length=128, help_text="종관기상관측 센터 지역이름")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
