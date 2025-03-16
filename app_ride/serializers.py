"""
Ride app Serializers
"""
from typing import List
from app_ride_event.serializers import RideEventSerializer
from app_user.serializers import UserSerializer
from .models import Ride
from rest_framework import serializers
from django.utils.timezone import now, timedelta


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        
    def validate(self, data):
        """
        Extra validation
        """
        # Checks if the roles of driver_id and rider_id matches in the user roles
        driver = data.get('driver')
        rider = data.get('rider')
        if driver is not None and getattr(driver, 'role', None) != 'driver':
            raise serializers.ValidationError({'message': 'Selected driver does not have the role \'driver\'.'})
        
        if rider is not None and getattr(rider, 'role', None) != 'rider':
            raise serializers.ValidationError({'message': 'Selected rider does not have the role \'rider\'.'})
        return data

    def create(self, validated_data):
        """
        Create ride and return data
        """
        return Ride.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update ride and return data
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save(update_fields=validated_data.keys())
        return instance
    

class RideListSerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()
    distance = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Ride
        fields = '__all__'
        
    def get_todays_ride_events(self, obj) -> List[str]:
        recent_events = obj.ride_event.filter(created_at__gte=now() - timedelta(hours=24))
        return RideEventSerializer(recent_events, many=True).data