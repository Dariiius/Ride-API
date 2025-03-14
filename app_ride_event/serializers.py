"""
Ride Event app Serializers
"""
from .models import RideEvent
from rest_framework import serializers
from django.utils.timezone import now


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'

    def create(self, validated_data):
        """
        Create ride event and return data
        """
        return RideEvent.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update ride event and return data
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save(update_fields=validated_data.keys())
        return instance