from django.db import models


class StationLocation(models.Model):
    class Provinces(models.TextChoices):
        SEOUL = "SEOUL", "서울"
        GYUNGGI = "GG", "경기도"
        INCHOEN = "INCHOEN", "인천"
        JEJU = "JEJU", "제주"
        GANGWON = "GW", "강원도"
        CHUNGBUK = "CB", "충북"
        CHUNGNAM = "CN", "충남"
        GYEONGBUK = "GB", "경북"
        GYEONGNAM = "GN", "경남"
        JEONBUK = "JB", "전북"
        JEONNAM = "JN", "전남"
        DAEGU = "DAEGU", "대구"
        DAESAN = "DAESAN", "대전"
        BUSAN = "BUSAN", "부산"
        ULSAN = "ULSAN", "울산"
        SEJONG = "SEJONG", "세종"

    station_name = models.CharField(max_length=128, help_text="종관기상관측 센터 지역이름")
    kma_station_code = models.CharField(max_length=8, help_text="종관기상관측 센터 코드")
    station_authority = models.CharField(max_length=128, help_text="종관기상관측 센터 관할지역")
    province = models.CharField(max_length=8, choices=Provinces.choices, help_text="종관기상관측 센터 관할지역")
    late_models_changed_at = models.DateTimeField(null=True, blank=True, help_text="최근 예측모델 변경 시간")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    """
        239	세종	대전지방기상청
        105	강릉	강원지방기상청
        108	서울	수도권기상청
        189	서귀포  제주지방기상청
        295	남해	부산지방기상청
    """

    def __str__(self):
        return f"{self.station_name} - {self.station_authority}"

    class Meta:
        verbose_name_plural = "StationLocations"


class Weather(models.Model):
    location = models.ForeignKey("StationLocation", on_delete=models.CASCADE, related_name="weather_location")
    date = models.DateField()
    min_temp = models.CharField(max_length=6)
    max_temp = models.CharField(max_length=6)
    total_rain = models.CharField(max_length=6)
    avg_humidity = models.CharField(max_length=6)
    wind_speed = models.CharField(max_length=6)
    wind_direction = models.CharField(max_length=6)
    avg_pa = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.indexes.Index(fields=["location", "date"], name="ix_weather_location_date_time"),
        ]

    @classmethod
    def get_data_range(cls, location: StationLocation):
        return cls.objects.filter(location=location).aggregate(min_date=models.Min("date"), max_date=models.Max("date"))

    @classmethod
    def get_last_data(cls, location: StationLocation):
        return cls.objects.filter(location=location).order_by("-date").first()


class WeatherPredictModel(models.Model):
    location = models.ForeignKey("StationLocation", on_delete=models.RESTRICT, related_name="weather_predict_model")
    start_date = models.DateField()
    end_date = models.DateField()
    model_file_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.indexes.Index(fields=["location", "created_at"], name="ix_predict_loc_created_at"),
        ]
        ordering = ["-created_at"]

    @classmethod
    def get_revision(cls, location):
        latest_model = cls.objects.filter(location=location).first()
        if not latest_model:
            return 1
        else:
            remove_ext = latest_model.model_file_name.split(".")[0]
            rev = remove_ext.split("_")[-1]
            return int(rev) + 1
