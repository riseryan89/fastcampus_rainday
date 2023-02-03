import datetime

from django.shortcuts import render

from app.models import StationLocation
from app.schedulers.prediction import create_model, predict
from app.schedulers.weather_data_collector import collect_load_weather_data


def index(request):
    station_location = StationLocation.objects.get(kma_station_code="108")
    # collect_load_weather_data(station_location, "20190503", "20221231")
    # create_model(
    #     station_location, datetime.datetime(2015, 1, 1, 0, 0, 0).date(), datetime.datetime(2022, 12, 31, 0, 0, 0).date()
    # )
    predict(station_location, datetime.datetime(2021, 1, 1, 0, 0, 0).date())
    return render(request, "index.html")
