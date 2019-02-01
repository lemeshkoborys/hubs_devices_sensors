from django.urls import path
from .views import (
    SensorListAPIView,
    DeviceListAPIView,
    HubListAPIView,
    HubsCollectedDataListAPIView,
    SensorCollectedDataListCreateAPIView,
    SensorCollectedDataAPIView
)

urlpatterns = [
    path('sensors/', SensorListAPIView.as_view(), name='sensor-list'),
    path(
        'sensors/collect-data/',
        SensorCollectedDataListCreateAPIView.as_view(), 
        name='sensors-collected-data-list'),
    path(
        'sensors/collected-data/',
        SensorCollectedDataAPIView.as_view(),
        name='hubs-collect-data'),
    path('devices/', DeviceListAPIView.as_view(), name='device-list'),
    path('hubs/', HubListAPIView.as_view(), name='hub-list'),
    path('hubs/collected-data/', HubsCollectedDataListAPIView.as_view(), name='hubs-collected-data-list')
]