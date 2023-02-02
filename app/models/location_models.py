from django.db import models

from app.models import User


class Location(models.Model):
    class Province(models.TextChoices):
        SEOUL = "SEOUL"
        INCHEON = "INCHEON"
        GYUNGGI = "GYUNGGI"
        JEJU = "JEJU"
        BUSAN = "BUSAN"

    province = models.CharField(max_length=10, choices=Province.choices, default=Province.SEOUL)
    location = models.CharField(max_length=128, help_text="종관기상관측 센터 지역이름")
    kma_location_id = models.CharField(max_length=10, help_text="기상청 종관기상관측 지점 ID")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
