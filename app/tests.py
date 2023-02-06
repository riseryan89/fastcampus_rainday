import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from app.forms.auth_forms import LoginForm, SignupForm

from app.models import Weather, StationLocation


class WeatherModelTest(TestCase):
    def setUp(self):
        self.station = StationLocation.objects.create(
            station_name="test_station",
            kma_station_code="108",
            station_authority="test",
            province=StationLocation.Provinces.SEOUL,
        )

        Weather.objects.create(
            location_id=1,
            date=datetime.date(2021, 1, 1),
            min_temp=10,
            max_temp=10,
            total_rain=10,
            avg_humidity=10,
            wind_speed=10,
            wind_direction=10,
            avg_pa=10,
        )

    def test_weather_model(self):
        date_range = Weather.get_data_range(self.station)
        self.assertEqual(date_range["min_date"], datetime.date(2021, 1, 1))
        self.assertEqual(date_range["max_date"], datetime.date(2021, 1, 1))


class AuthFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test@test.com",
            password="test1234",
        )

    def test_login_form(self):
        form = LoginForm(data={"username": "test", "password": "test1234"})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = LoginForm(data={"username": "test", "password": "test12345"})
        self.assertFalse(form.is_valid())

    def test_login_form_invalid_username(self):
        form = LoginForm(data={"username": "test1", "password": "test1234"})
        self.assertFalse(form.is_valid())

    def test_register_form(self):
        form = SignupForm(
            {"username": "test1", "email": "t@test.com", "password1": "aaa123fff", "password2": "aaa123fff"}
        )
        self.assertTrue(form.is_valid())
