"""
Ride Event app Serializers
"""
from .models import RideEvent
from rest_framework import serializers


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'
        
    def validate(self, data):
        """
        Extra validation
        """
        request = self.context.get('request')
        
        # Checks if the ride already has an existing event in a POST request
        if request and request.method == 'POST':
            if RideEvent.objects.filter(ride_id=data.get('ride')).exists():
                raise serializers.ValidationError({'message': 'A ride event already exists for this ride.'})
        return data

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