"""
Ride Event app Views
"""
from .models import RideEvent
from .serializers import RideEventSerializer
from app_user.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Ride Events'])
class RideEventView(viewsets.ModelViewSet):
    """
    Ride Event View
    """
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def list(self, request, *args, **kwargs):
        """
        Get list of ride event
        """
        serializer = self.get_serializer(self.paginate_queryset(self.queryset), many=True)
        return self.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Get specific ride event
        """
        ride_event = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(ride_event)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create new ride event
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                {'message': 'New ride event has been created successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        """
        Partially update existing ride event using given data
        """
        ride = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(ride, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                {'message': 'Ride event has been updated successfully.'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete specific ride event
        """
        ride = get_object_or_404(self.queryset, pk=pk)
        ride.delete()
        return Response(
            {'message': 'Ride event has been deleted successfully.'},
            status=status.HTTP_200_OK
        )