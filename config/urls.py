from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


#Static Url Configuration
from django.conf import settings
from django.conf.urls.static import static

def welcome(request):
    return JsonResponse(
        {
            "name": "Emcent Project",
            "url": "https://weatherapi-production-bbf2.up.railway.app/v1/auth/",
            "message": "Welcome to my project",
            "status": 200,
        }
    )


schema_view = get_schema_view(
    openapi.Info(
        title="My Documentation",
        default_version='v1',
        description="This is the doc to my project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mcinnobezzy@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('', welcome),
    path('v1/auth/', include("accounts.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('weather-api/', include('weatherapi.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)