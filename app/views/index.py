import datetime
import random

import requests
from django.shortcuts import render

from app.models import StationLocation, Weather
from app.schedulers.prediction import create_model, predict
from app.schedulers.weather_data_collector import collect_load_weather_data


def index(request):

    # collect_load_weather_data(station_location, "20190503", "20221231")
    # create_model(
    #     station_location, datetime.datetime(2015, 1, 1, 0, 0, 0).date(), datetime.datetime(2022, 12, 31, 0, 0, 0).date()
    # )
    # is_rain = predict(station_location, datetime.datetime(2021, 1, 1, 0, 0, 0).date())

    res = requests.get(f"http://ip-api.com/json/{get_client_ip(request)}")
    region = res.json()["regionName"]

    has_region = True
    if region == "Gyeonggi-do":
        kma_station_code = "133"
    elif region == "Seoul":
        kma_station_code = "108"
    else:
        kma_station_code = "108"
        has_region = False
    station_location = StationLocation.objects.get(kma_station_code=kma_station_code)
    last_5_data = Weather.objects.filter(location=station_location).order_by("-date")[:5]
    context = {
        "hello": "hello world",
        "region": region,
        "has_region": has_region,
        "last_5_data": last_5_data,
    }
    return render(request, "index.html", context)


def get_client_ip(request):
    x_forwarded_for = request.headers.get("x-appengine-user-ip")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
        if ip == "127.0.0.1":
            return "12.233.22.33"
    return ip
