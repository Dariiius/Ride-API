"""
Ride app admin config
"""
from django.contrib import admin
from .models import Ride


class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'rider', 'status')   
    list_filter = ('status',)
    search_fields = ('driver__email', 'rider__email')


admin.site.register(Ride, RideAdmin)