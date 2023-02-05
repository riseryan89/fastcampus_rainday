import datetime
import random

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


def test_view(request):
    show_header = True
    today = datetime.datetime(2022, 1, 1, 11, 11, 11)
    items = ["item 1", "item 2", "item 3", "item 4", "item 5", "item 6"]
    var = None
    long_string = "이 문장은 매우 매우 매우 긴 문장입니다. 그래서 아쉽게도 Truncate 될 예정 입니다."
    string = "Upper or lower?"
    list_of_strings = ["string 1", "string 2", "string 3"]
    boolean_value = True
    random_number = random.randint(1, 1000)
    context = {
        "show_header": show_header,
        "today": today,
        "items": items,
        "var": var,
        "long_string": long_string,
        "string": string,
        "list_of_strings": list_of_strings,
        "boolean_value": boolean_value,
        "random_number": random_number,
    }
    return render(request, "test.html", context)


def test_view2(request, arg1, arg2):
    return render(request, "test.html", {})
