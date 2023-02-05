from django.contrib import admin
from django.urls import path

from app import views as v

urlpatterns = [
    path("", v.index, name="home"),
    path("auth/login", v.user_login, name="login"),
    path("auth/logout", v.user_logout, name="logout"),
    path("auth/signup", v.user_signup, name="signup"),
]
