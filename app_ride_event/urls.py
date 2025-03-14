"""
Ride Event app URL config
"""
from django.urls import path, include
from rest_framework import routers
from .views import RideEventView


router = routers.DefaultRouter()
router.register('', RideEventView, basename='ride_event')

urlpatterns = [
    path('', include(router.urls))
]