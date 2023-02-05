import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from app.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
        error_messages={
            "invalid_login": "잘못된 유저네임 이잖아~~",
        },
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )


class SignupForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
        error_messages={
            "invalid": "잘못된 이메일 이잖아~~",
        },
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}), label="Password1"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password 확인"}),
        label="Password2",
        error_messages={
            "password_mismatch": "비밀번호가 일치하지 않습니다.",
        },
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean(self):
        username = self.cleaned_data.get("username")

        if not re.match("^[a-z0-9_]*$", username):
            self.add_error("username", "소문자와, 숫자, 언더스코어(_) 만 사용가능!")
