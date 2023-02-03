from django.shortcuts import render

from app.models import StationLocation
from app.schedulers.weather_data_collector import collect_load_weather_data


def index(request):
    station_location = StationLocation.objects.get(kma_station_code="239")
    collect_load_weather_data(station_location, "20210801", "20210810")
    return render(request, "index.html")
