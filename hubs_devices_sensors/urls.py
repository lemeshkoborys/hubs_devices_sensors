"""
urls.py
Contains routing for hubs_devices_sensors app
"""
from django.urls import path
from .views import (
    SensorListCreateAPIView,
    DeviceListCreateAPIView,
    HubListAPIView,
    HubCreateAPIView,
    SensorCollectedDataListCreateAPIView,
    SensorCollectedDataAdminAPIView,
    SensorCollectedDataUserAPIView
)

"""
Available API paths:
    sensors/ - GET, POST
    sensors/collect-data/ - POST
    sensors/collected-data/admin/ - GET
    sensors/collected-data/ - GET
    devices/ - GET, POST
    hubs/ - GET
    hubs/create/ - POST
"""

urlpatterns = [
    path('sensors/', SensorListCreateAPIView.as_view(), name='sensor-list-create'),
    path(
        'sensors/collect-data/',
        SensorCollectedDataListCreateAPIView.as_view(),
        name='sensors-collect-data'),
    path(
        'sensors/collected-data/admin/',
        SensorCollectedDataAdminAPIView.as_view(),
        name='sensors-collect-data-admin'),
    path(
        'sensors/collected-data/',
        SensorCollectedDataUserAPIView.as_view(),
        name='sensors-collect-data'
    ),
    path('devices/', DeviceListCreateAPIView.as_view(), name='device-list'),
    path('hubs/', HubListAPIView.as_view(), name='hub-list'),
    path('hubs/create/', HubCreateAPIView.as_view(), name='hub-create'),        
]
