"""
Ride app Serializers
"""
from app_ride_event.serializers import RideEventSerializer
from app_user.serializers import UserSerializer
from .models import Ride
from rest_framework import serializers
from django.utils.timezone import now


class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)
    ride_events = RideEventSerializer(source='ride', many=True, read_only=True)
    
    class Meta:
        model = Ride
        fields = '__all__'

    def create(self, validated_data):
        """
        Create ride and return data
        """
        return Ride.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update ride and return data
        """
        if 'status' in validated_data and validated_data['status'] == 'pickup':
            validated_data['pickup_time'] = now()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save(update_fields=validated_data.keys())
        return instance