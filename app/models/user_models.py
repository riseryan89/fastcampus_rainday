from typing import List, Union

from django.db import models
from django.contrib.auth.models import AbstractUser

from app.models.weather_models import StationLocation


class User(AbstractUser):
    locations = models.ManyToManyField("StationLocation", related_name="user_location")

    def __str__(self):
        return self.username

    def refresh_subscriptions(self, selected_locations: List[Union[int, str]]):
        self.locations.clear()
        if selected_locations:
            location = StationLocation.objects.filter(id__in=selected_locations)
            self.locations.set(location)

    def subscribed_location_ids(self):
        return self.locations.values_list("id", flat=True)
