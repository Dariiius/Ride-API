"""
RIDE-API URL config
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    # Main urls
    path('admin/', admin.site.urls),
    path('rides/', include('app_ride.urls')),
         
    # Documentation
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
