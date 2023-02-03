from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from app.forms.auth_forms import LoginForm, SignupForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "auth/signup.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")
