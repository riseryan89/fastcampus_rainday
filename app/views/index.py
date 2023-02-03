import datetime

import requests
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
    # is_rain = predict(station_location, datetime.datetime(2021, 1, 1, 0, 0, 0).date())

    res = requests.get(f"http://ip-api.com/json/{get_client_ip(request)}")
    context = {
        "hello": "hello world",
        "city": res.json()["regionName"],
    }
    return render(request, "index.html", context)


def get_client_ip(request):
    x_forwarded_for = request.headers.get("x-appengine-user-ip")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
        if ip == "127.0.0.1":
            return "1.233.22.33"
    return ip
