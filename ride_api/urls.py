"""
RIDE-API URL config
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema

from ride_api import settings


token_obtain_schema_view = extend_schema_view(
    post=extend_schema(tags=['Authentication'])
)(TokenObtainPairView.as_view())

token_refresh_schema_view = extend_schema_view(
    post=extend_schema(tags=['Authentication'])
)(TokenRefreshView.as_view())

urlpatterns = [
    # Main urls
    path('admin/', admin.site.urls),
    path('api/user/', include('app_user.urls')),
    path('api/ride/', include('app_ride.urls')),
    path('api/rideevent/', include('app_ride_event.urls')),
         
    # Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Token
    path('api/token/', token_obtain_schema_view, name='token_obtain_pair'),
    path('api/token/refresh/', token_refresh_schema_view, name='token_refresh'),
] 

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns += debug_toolbar_urls()