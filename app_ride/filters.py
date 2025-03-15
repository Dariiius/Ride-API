"""
Ride app Filters
"""
from django_filters import rest_framework as filters
from .models import Ride


class RideFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Ride.STATUS)
    rider_email = filters.CharFilter(field_name='rider__email', lookup_expr='iexact')
    
    class Meta:
        model = Ride
        fields = ['status', 'rider_email']