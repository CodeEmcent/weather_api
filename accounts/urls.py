from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('user', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', user_login)
]