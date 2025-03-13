"""
User app Views
"""
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Users"])
class UserView(viewsets.ModelViewSet):
    """
    User View
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def list(self, request, *args, **kwargs):
        """
        Get list of users
        """
        serializer = self.get_serializer(self.queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
    
    def retrieve(self, request, pk=None):
        """
        Get specific user
        """
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create new user
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                {'message': 'New user has been created successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        """
        Partially update existing user using given data
        """
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                {'message': 'User has been updated successfully.'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete specific user
        """
        user = get_object_or_404(self.queryset, pk=pk)
        user.delete()
        return Response(
            {'message': 'User has been deleted successfully.'},
            status=status.HTTP_200_OK
        )