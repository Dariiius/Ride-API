"""
Ride app URL config
"""
from django.urls import path, include
from rest_framework import routers
from app_ride.views import RideView


router = routers.DefaultRouter()
router.register('', RideView, basename='ride')

urlpatterns = [
    path('', include(router.urls))
]