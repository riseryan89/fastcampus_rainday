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
    num_of_rows = 10
    data_type = "JSON"
    data_cd = "ASOS"
    date_cd = "DAY"
    start_dt = start_date
    end_dt = end_date if end_date else start_date
    stn_ids = station_location.kma_station_code

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
                "date": item["tm"],
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
