"""
User app Views
"""
from app_ride.models import Ride
from app_ride.serializers import RideSerializer
from app_user.permissions import IsAdminUser
from .filters import RideFilter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django_filters import rest_framework as filters


@extend_schema(tags=['Rides'])
class RideView(viewsets.ModelViewSet):
    """
    Ride View
    """
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RideFilter
    
    def list(self, request, *args, **kwargs):
        """
        Get list of rides
        """
        queryset = self.filter_queryset(self.queryset)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
    
    def retrieve(self, request, pk=None):
        """
        Get specific ride
        """
        ride = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(ride)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create new ride
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                {'message': 'New ride has been created successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        """
        Partially update existing ride using given data
        """
        ride = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(ride, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                {'message': 'Ride has been updated successfully.'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete specific ride
        """
        ride = get_object_or_404(self.queryset, pk=pk)
        ride.delete()
        return Response(
            {'message': 'Ride has been deleted successfully.'},
            status=status.HTTP_200_OK
        )