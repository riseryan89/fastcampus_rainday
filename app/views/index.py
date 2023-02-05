import datetime
import random

import requests
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from app.forms.auth_forms import LoginForm, SignupForm
from app.forms.subscribe_form import LocationSubscribeForm
from app.models import StationLocation, Weather
from app.schedulers.prediction import create_model, predict
from app.schedulers.weather_data_collector import collect_load_weather_data


def index(request):

    station_id = request.GET.get("station_id")
    res = requests.get(f"http://ip-api.com/json/{get_client_ip(request)}")
    region = res.json()["regionName"]
    selected_region = None
    has_region = True
    all_location = StationLocation.objects.all()
    if region == "Gyeonggi-do":
        kma_station_code = "133"
    elif region == "Seoul":
        kma_station_code = "108"
    else:
        kma_station_code = "108"
        has_region = False
    if station_id:
        station_location = StationLocation.objects.get(id=station_id)
        kma_station_code = station_location.kma_station_code
        selected_region = station_location.station_name
        has_region = None

    station_location = StationLocation.objects.get(kma_station_code=kma_station_code)
    last_5_data = Weather.objects.filter(location=station_location).order_by("-date")[:5]
    if request.user.is_authenticated:
        subscribed_locations = request.user.locations.all().values_list("id", flat=True)
        subscribe_form = LocationSubscribeForm(initial={"checkbox_field": list(subscribed_locations)})
    else:
        subscribe_form = LocationSubscribeForm()
    context = {
        "hello": "hello world",
        "region": region,
        "selected_region": selected_region,
        "has_region": has_region,
        "last_5_data": last_5_data,
        "auth_form": LoginForm(),
        "signup_form": SignupForm(),
        "subscribe_form": subscribe_form,
        "locations": all_location,
        "form_error": "",
        "initial_data": [],
        "prediction": predict(station_location),
    }

    if request.method == "POST":
        submit_type = request.GET.get("type")

        if submit_type == "signup":
            context["signup_form"] = SignupForm(data=request.POST)
            form = SignupForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect("home")
            else:
                context["form_error"] = "signup"

        elif submit_type == "login":
            form = LoginForm(data=request.POST)
            context["auth_form"] = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("home")
            else:
                context["form_error"] = "login"

        elif submit_type == "subscription":
            form = LocationSubscribeForm(data=request.POST)
            selected_locations = form.data.get("checkbox_field", [])
            request.user.locations.clear()
            if selected_locations:
                location = StationLocation.objects.filter(id__in=selected_locations)
                request.user.locations.set(location)
            return redirect("home")

        return render(request, "index.html", context)

    else:
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
