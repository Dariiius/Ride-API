"""
User app Serializers
"""
from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'phone_number', 'password', 'password2']

    def validate(self, data):
        """
        Extra validation
        """
        # Checks if the two passwords match
        if 'password' in data or 'password2' in data:
            if data['password'] != data['password2']:
                raise serializers.ValidationError({'message': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        """
        Create user and return data
        """
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)
        user.username = validated_data['email']
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Update user and return data
        """
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)
        
        email = validated_data.pop('email', None)
        if email:
            instance.email = email
            instance.username = email
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
            if attr == 'email':
                setattr(instance, 'username', value)
            
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance