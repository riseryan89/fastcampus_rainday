from datetime import datetime, timedelta
from app.models import StationLocation
from app.schedulers import db_auto_reconnect
from app.utils import collect_load_weather_data


@db_auto_reconnect
def scheduled_collection():
    print("scheduled_collection")
    station_locations = StationLocation.objects.all()
    utc = datetime.utcnow()
    kst = utc + timedelta(hours=9)
    today = kst.date()
    start_date = today - timedelta(days=7)
    end_date = today - timedelta(days=1)
    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")
    for station_location in station_locations:
        try:
            collect_load_weather_data(station_location, start_date_str, end_date_str)
            print(f"SUCCESS: {station_location.station_name}")
        except Exception as e:
            print("ERROR")
            print("Cannot collect weather data for station location: ", station_location)
            raise e
