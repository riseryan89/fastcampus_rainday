from django.contrib import admin
from django.urls import path

from app import views as v

urlpatterns = [
    path("", v.index, name="home"),
    path("test", v.test_view, name="test"),
    path("test2/<str:arg1>/<str:arg2>", v.test_view2, name="test2"),
    path("auth/login", v.user_login, name="login"),
    path("auth/logout", v.user_login, name="logout"),
    path("auth/signup", v.user_signup, name="signup"),
]
