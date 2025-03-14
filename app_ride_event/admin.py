"""
Ride Event app admin config
"""
from django.contrib import admin
from .models import RideEvent


class RideEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'ride', 'description', 'created_at')   
    list_filter = ('created_at',)
    search_fields = ('ride__driver__email', 'ride__rider__email', 'description')


admin.site.register(RideEvent, RideEventAdmin)