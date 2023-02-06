from app.models import StationLocation, Weather
from app.schedulers import db_auto_reconnect
from app.utils import create_model


@db_auto_reconnect
def update_model():
    for station_location in StationLocation.objects.all():
        date_range = Weather.get_data_range(station_location)
        create_model(station_location, date_range.get("min_date"), date_range.get("max_date"))
        print(f"SUCCESS MODEL UPDATE: {station_location.station_name}")
    # 코드 from app/utils/create_model.py:
