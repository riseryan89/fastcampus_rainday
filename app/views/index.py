from django.shortcuts import render

from app.models import StationLocation
from app.schedulers.prediction import create_model
from app.schedulers.weather_data_collector import collect_load_weather_data


def index(request):
    station_location = StationLocation.objects.get(kma_station_code="108")
    # collect_load_weather_data(station_location, "20200201", "20221231")
    # create_model()
    return render(request, "index.html")
