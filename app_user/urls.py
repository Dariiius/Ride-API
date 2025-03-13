"""
User app URL config
"""
from django.urls import path, include
from .views import UserView
from rest_framework import routers


router = routers.DefaultRouter()
router.register('', UserView, basename='user')

urlpatterns = [
    path('', include(router.urls))
]