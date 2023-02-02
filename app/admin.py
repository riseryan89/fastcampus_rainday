from django.contrib import admin
import inspect
from app import models as m

# Register your models here.


admin.site.register(m.User)
admin.site.register(m.StationLocation)
admin.site.register(m.Weather)
