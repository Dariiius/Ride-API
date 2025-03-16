"""
User app models
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('rider', 'Rider'),
        ('driver', 'Driver'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default=ROLES[0][0])
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    email = models.EmailField(unique=True)