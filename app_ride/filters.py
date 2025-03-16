"""
Ride app Filters
"""
import math
from django_filters import rest_framework as filters
from .models import Ride
from django.db.models.expressions import ExpressionWrapper
from django.db.models.functions import Sin, Cos, ACos, Radians
from django.db.models import F, FloatField, Value
from rest_framework import serializers


class RideFilter(filters.FilterSet):
    SORT_BY = (
        ('pickup_time', 'Pickup Time'),
        ('distance', 'Distance'),
    )
    
    status = filters.ChoiceFilter(choices=Ride.STATUS)
    rider_email = filters.CharFilter(field_name='rider__email', lookup_expr='iexact')
    sort_by = filters.ChoiceFilter(choices=SORT_BY, method='filter_sort_by')
    origin_latitude = filters.NumberFilter(help_text='Origin\'s latitude', method=lambda q, n, v: q)
    origin_longitude  = filters.NumberFilter(help_text='Origin\'s longitude', method=lambda q, n, v: q)
    
    class Meta:
        model = Ride
        fields = ['status', 'rider_email', 'origin_latitude', 'origin_longitude']
        
    def filter_sort_by(self, queryset, name, value):
        if value == 'pickup_time':
            return queryset.order_by('pickup_time')
        elif value == 'distance':
            request = self.request
            origin_latitude = request.query_params.get('origin_latitude')
            origin_longitude = request.query_params.get('origin_longitude')
            
            if origin_latitude is None or origin_longitude is None:
                raise serializers.ValidationError(
                    {'message': 'Both \'origin_latitude\' and \'origin_longitude\' are required for distance sorting.'}
                ) 
                
            # Calculate distance from point A to point B using Haversine Formula (spherical law of cosines)
            try:
                origin_lat, origin_long = float(origin_latitude), float(origin_longitude)
                R = 6371 # Earth's radius by km
                
                queryset = queryset.annotate(
                    distance=ExpressionWrapper(
                        R * ACos(
                            Cos(Radians(Value(origin_lat))) * Cos(Radians(F('pickup_latitude'))) *
                            Cos(Radians(F('pickup_longitude')) - Radians(Value(origin_long))) +
                            Sin(Radians(Value(origin_lat))) * Sin(Radians(F('pickup_latitude')))
                        ),
                        output_field=FloatField()
                    )
                ).order_by('distance')
            except Exception as e:
                pass
            
        return queryset