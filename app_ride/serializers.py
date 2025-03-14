"""
Ride app Serializers
"""
from .models import Ride
from rest_framework import serializers
from django.utils.timezone import now


class RideSerializer(serializers.ModelSerializer):
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