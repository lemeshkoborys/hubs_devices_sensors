"""
urls.py
Contains routing for hubs_devices_sensors app
"""
from django.urls import path
from .views.sensors_collected_data_views import (
    SensorCollectedDataListCreateAPIView,
    SensorCollectedDataAdminAPIView,
    SensorAllCollectedDataUserAPIView,
    OneSensorCollectedDataUserAPIView
)
from .views.hub_views import (
    HubListAPIView,
    HubCreateAPIView,
    HubRetrieveUpateDestroyAPIView,
    HubDevicesListAPIView,
)

from .views.sensor_views import (
    SensorListAPIView,
    SensorCreateAPIView,
    SensorRetrieveUpdateDestroyAPIView
)
from .views.device_views import (
    DeviceCreateAPIView,
    DeviceListAPIView,
    DeviceRetrieveUpdateDestroy,
    DeviceListSensorsAPIView,
    DeviceSensorsCollectedDataTimeRangeAPIView
)


# Available API paths:
#     sensors/ - GET
#     sensors/create/ - POST
#     sensors/<int:pk>/ - GET, PUT, PATCH, DELETE
#     sensors/collect-data/ - POST
#     sensors/collected-data/admin/ - GET
#     sensors/collected-data/ - GET
#     sensors/<int:pk>/collected-data/ - GET
#     devices/ - GET
#     devices/create/ - POST
#     devices/<int:pk>/ - GET, PUT, PATCH, DELETE
#     devices/<int:pk>/sensors/ - GET
#     hubs/ - GET
#     hubs/create/ - POST
#     hubs/<int:pk>/ - GET, PUT, PATCH, DELETE
#     hubs/<int:pk>/devices/ - GET


urlpatterns = []

HUBS_URLS = [
    path('hubs/', HubListAPIView.as_view(), name='hub-list'),
    path('hubs/create/', HubCreateAPIView.as_view(), name='hub-create'),
    path(
        'hubs/<int:pk>/',
        HubRetrieveUpateDestroyAPIView.as_view(),
        name='hub-detail'
    ),
    path(
        'hubs/<int:pk>/devices/',
        HubDevicesListAPIView.as_view(),
        name='hub-devices'
    )
]

SENSORS_URLS = [
    path('sensors/', SensorListAPIView.as_view(), name='sensor-list'),
    path('sensors/create/', SensorCreateAPIView.as_view(), name='sensor-create'),
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
        name='sensor-detail'
    ),
]

DEVICES_URLS = [
    path('devices/', DeviceListAPIView.as_view(), name='device-list'),
    path('devices/create/', DeviceCreateAPIView.as_view(), name='device-create'),
    path(
        'devices/<int:pk>/',
        DeviceRetrieveUpdateDestroy.as_view(),
        name='device-detail'
    ),
    path(
        'devices/<int:pk>/sensors/',
        DeviceListSensorsAPIView.as_view(),
        name='device-sensors'
    ),
    path(
        # e.g ?start_datetime=2018-01-02T21:25:33Z&end_datetime=2018-01-02T22:45:33Z
        'devices/<int:pk>/sensors-collected-data/',
        DeviceSensorsCollectedDataTimeRangeAPIView.as_view(),
        name='sensor-data-time-range'
    )
]
urlpatterns += DEVICES_URLS + HUBS_URLS + SENSORS_URLS
