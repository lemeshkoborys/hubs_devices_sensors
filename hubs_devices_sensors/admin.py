from django.contrib import admin
from .models import Sensor, Device, Hub, SensorCollectedData

admin.site.register(Sensor)
admin.site.register(SensorCollectedData)
admin.site.register(Device)
admin.site.register(Hub)
