import pandas as pd
from django.db.models import F
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

from app.models import Weather


# Create a DataFrame with the data
def create_model():
    weather_queryset = Weather.objects.all().annotate(date_month=F("date__month")).order_by("date")
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

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(["total_rain", "tomorrow_total_rain_binary"], axis=1), df["tomorrow_total_rain_binary"], test_size=0.2
    )

    # Train a RandomForestRegressor on the training data
    regressor = RandomForestRegressor(n_estimators=100)
    regressor.fit(X_train, y_train)

    # Use the trained model to make predictions on the test data
    y_pred = regressor.predict(X_test)

    # Evaluate the model's performance by computing the accuracy
    accuracy = (y_pred > 0.5) == y_test
    print("Accuracy:", accuracy.mean())

    # Save the model to disk

    today_weather = (
        Weather.objects.annotate(date_month=F("date__month"))
        .order_by("date")
        .values(
            "date_month",
            "max_temp",
            "min_temp",
            "avg_humidity",
            "wind_speed",
            "wind_direction",
            "avg_pa",
        )
        .last()
    )
    print(today_weather)
    today_df = pd.DataFrame(today_weather, index=[0])

    today_prediction = regressor.predict(today_df)
    print(today_prediction)
    print(today_prediction)
