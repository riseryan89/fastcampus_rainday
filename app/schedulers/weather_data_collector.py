from datetime import date, datetime, timedelta
from typing import List

import requests
from django.db import models

from app.models import StationLocation, Weather


def collect_load_weather_data(station_location: StationLocation, start_date: str, end_date: str = None):
    """
    :return:
    """

    service_key = "V7hxbl/SgKx2csniM4ByG+qpow1xfjIF1097ib8HEkA1htaEDnIC90IYTMDkgOXnxr4yl03wYtioTuyaP7tEvQ=="
    page_num = 1
    num_of_rows = 30
    data_type = "JSON"
    data_cd = "ASOS"
    date_cd = "DAY"
    start_dt = start_date
    end_dt = end_date if end_date else start_date
    stn_ids = station_location.kma_station_code

    date_range = []
    # if the gap between start date and end date is more than 1 month, split the date range into 1 month and append to date_range as a tuple
    if (datetime.strptime(end_dt, "%Y%m%d").date() - datetime.strptime(start_dt, "%Y%m%d").date()).days > 30:
        start_date = datetime.strptime(start_dt, "%Y%m%d").date()
        end_date = datetime.strptime(end_dt, "%Y%m%d").date()
        while start_date <= end_date:
            done = False
            if start_date + timedelta(days=30) > end_date:
                end_date_str = end_date.strftime("%Y%m%d")
                done = True
            else:
                end_date_str = (start_date + timedelta(days=30)).strftime("%Y%m%d")
            date_range.append((start_date.strftime("%Y%m%d"), end_date_str))
            start_date = start_date + timedelta(days=31)
            if done:
                break
    else:
        date_range.append((start_dt, end_dt))
    print(date_range)
    for start_dt, end_dt in date_range:
        query_string = {
            "serviceKey": service_key,
            "pageNo": page_num,
            "numOfRows": num_of_rows,
            "dataType": data_type,
            "dataCd": data_cd,
            "dateCd": date_cd,
            "startDt": start_dt,
            "endDt": end_dt,
            "stnIds": stn_ids,
        }
        url = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
        response = requests.get(url, params=query_string)
        res = response.json()
        print(res)
        is_ok = check_status(res)
        if is_ok:
            result: List[dict] = parse_data(res)
            result.sort(key=lambda x: x["date"])
            print(result)


def check_status(res: dict) -> bool:
    if res["response"]["header"]["resultCode"] == "00":
        print("SUCCESS")
        return True
    else:
        print("FAIL")
        print(res["response"]["header"]["resultMsg"], res["response"]["header"]["resultCode"])
        return False


def parse_data(res):
    result = []
    for item in res["response"]["body"]["items"]["item"]:
        result.append(
            {
                "date": datetime.strptime(item["tm"], "%Y-%m-%d").date(),
                "min_temp": item["minTa"] if item["minTa"] else "0",
                "max_temp": item["maxTa"] if item["maxTa"] else "0",
                "total_rain": item["sumRn"] if item["sumRn"] else "0",
                "avg_humidity": item["avgRhm"] if item["avgRhm"] else "0",
                "wind_speed": item["avgWs"] if item["avgWs"] else "0",
                "wind_direction": item["maxWd"] if item["maxWd"] else "0",
                "avg_pa": item["avgPa"] if item["avgPa"] else "0",
            }
        )
    return result
