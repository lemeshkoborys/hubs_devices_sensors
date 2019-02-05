"""
urls.py
Contains routing for hubs_devices_sensors app
"""
from django.urls import path
from .views import (
    SensorListCreateAPIView,
    SensorRetrieveUpdateDestroyAPIView,
    DeviceListCreateAPIView,
    DeviceRetrieveUpdateDestroy,
    HubListAPIView,
    HubCreateAPIView,
    HubRetrieveUpateDestroyAPIView,
    SensorCollectedDataListCreateAPIView,
    SensorCollectedDataAdminAPIView,
    SensorAllCollectedDataUserAPIView,
    OneSensorCollectedDataUserAPIView
)

"""
Available API paths:
    sensors/ - GET
    sensors/create/ - POST
    sensors/<int:pk>/ - GET
    sensors/<int:pk>/update/ - PUT, PATCH
    sensors/<int:pk>/delete/ - DELETE 
    sensors/collect-data/ - POST
    sensors/collected-data/admin/ - GET
    sensors/collected-data/ - GET
    sensors/<int:pk>/collected-data/ - GET
    devices/ - GET
    devices/create/ - POST
    devices/<int:pk>/ - GET
    devices/<int:pk>/update - PUT, PATCH
    devices/<int:pk>/delete - DELETE
    hubs/ - GET
    hubs/create/ - POST
    hubs/<int:pk>/ - GET
    hubs/<int:pk>/update/ - PUT, PATCH
    hubs/<int:pk>/delete/ - DELETE
"""

urlpatterns = []

HUBS_URLS = [
    path('hubs/', HubListAPIView.as_view(), name='hub-list'),
    path('hubs/create/', HubCreateAPIView.as_view(), name='hub-create'),
    path(
        'hubs/<int:pk>/',
        HubRetrieveUpateDestroyAPIView.as_view(),
        name='hub-retrieve'
    ),
    path(
        'hubs/<int:pk>/update/',
        HubRetrieveUpateDestroyAPIView.as_view(),
        name='hub-update'
    ),
    path(
        'hubs/<int:pk>/delete/',
        HubRetrieveUpateDestroyAPIView.as_view(),
        name='hub-delete'
    )
]

SENSORS_URLS = [
    path('sensors/', SensorListCreateAPIView.as_view(), name='sensor-list'),
    path('sensors/create/', SensorListCreateAPIView.as_view(), name='sensor-create'),
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
        SensorAllCollectedDataUserAPIView.as_view(),
        name='sensors-collect-data'
    ),
    path(
        'sensors/<int:pk>/collected-data/',
        OneSensorCollectedDataUserAPIView.as_view(),
        name='sensor-collected-data'
    ),
    path(
        'sensors/<int:pk>/',
        SensorRetrieveUpdateDestroyAPIView.as_view(),
        name='sensor-retrieve'
    ),
    path(
        'sensors/<int:pk>/update/',
        SensorRetrieveUpdateDestroyAPIView.as_view(),
        name='sensor-update'
    ),
    path(
        'sensors/<int:pk>/delete/',
        SensorRetrieveUpdateDestroyAPIView.as_view(),
        name='sensor-delete'
    ),
    

]

DEVICES_URLS = [
    path('devices/', DeviceListCreateAPIView.as_view(), name='device-list'),
    path('devices/create/', DeviceListCreateAPIView.as_view(), name='device-create'),
    path(
        'devices/<int:pk>/',
        DeviceRetrieveUpdateDestroy.as_view(),
        name='device-retrieve'
    ),
    path(
        'devices/<int:pk>/update/',
        DeviceRetrieveUpdateDestroy.as_view(),
        name='device-update'
    ),
]
urlpatterns += DEVICES_URLS + HUBS_URLS + SENSORS_URLS
