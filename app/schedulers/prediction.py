from datetime import date

import pandas as pd
from django.db.models import F
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

from app.models import Weather, StationLocation, WeatherPredictModel
from rainday.settings import BASE_DIR


def create_model(station_location: StationLocation, start_date: date, end_date: date):
    weather_queryset = (
        Weather.objects.filter(location=station_location, date__gte=start_date, date__lte=end_date)
        .annotate(date_month=F("date__month"))
        .order_by("date")
    )
    df = pd.DataFrame.from_records(
        weather_queryset.values(
            "date_month",
            "max_temp",
            "min_temp",
            "total_rain",
            "avg_humidity",
            "wind_speed",
            "wind_direction",
            "avg_pa",
        )
    )
    df["tomorrow_total_rain_binary"] = (df["total_rain"].astype(float) > 0).astype(int)
    df["tomorrow_total_rain_binary"].shift(-1)

    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(["total_rain", "tomorrow_total_rain_binary"], axis=1), df["tomorrow_total_rain_binary"], test_size=0.2
    )

    regressor = RandomForestRegressor(n_estimators=100)
    regressor.fit(X_train, y_train)

    # y_pred = regressor.predict(X_test)
    # accuracy = (y_pred > 0.5) == y_test
    # print("Accuracy:", accuracy.mean())

    rev = WeatherPredictModel.get_revision(station_location)

    joblib.dump(regressor, BASE_DIR / f"app/prediction_models/models_station_{station_location.pk}_{rev}.pkl")
    WeatherPredictModel.objects.create(
        location=station_location,
        start_date=start_date,
        end_date=end_date,
        model_file_name=f"models_station_{station_location.pk}_{rev}.pkl",
    )
