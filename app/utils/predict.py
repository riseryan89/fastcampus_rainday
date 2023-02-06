from datetime import datetime, date, timedelta

import joblib
import pandas as pd
from django.db.models import F

from app.models import StationLocation, WeatherPredictModel, Weather
from app.utils.create_model import create_model
from rainday.settings import BASE_DIR


def predict(station_location: StationLocation, date_: date = None):
    if not date_:
        yesterday = Weather.get_last_data(station_location).date
    else:
        yesterday = date_ - timedelta(days=1)

    model = WeatherPredictModel.objects.filter(location=station_location).first()
    if not model:
        date_range = Weather.get_data_range(station_location)
        create_model(station_location, date_range.get("min_date"), date_range.get("max_date"))
        model = WeatherPredictModel.objects.filter(location=station_location).first()

    regressor = joblib.load(BASE_DIR / f"app/prediction_models/{model.model_file_name}")

    yesterday_weather = Weather.objects.filter(location=station_location, date=yesterday).annotate(
        date_month=F("date__month")
    )
    today_weather = yesterday_weather.values(
        "date_month",
        "max_temp",
        "min_temp",
        "avg_humidity",
        "wind_speed",
        "wind_direction",
        "avg_pa",
    ).first()
    today_df = pd.DataFrame(today_weather, index=[0])

    today_prediction = regressor.predict(today_df)
    if today_prediction > 0.5:
        return True
    return False
