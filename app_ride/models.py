"""
Ride app models
"""
from django.db import models
from app_user.models import User


class Ride(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('en-route', 'En-route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff')
    )
    
    status = models.CharField(max_length=10, choices=STATUS, default=STATUS[0][0])
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rider')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField(null=True, blank=True)
