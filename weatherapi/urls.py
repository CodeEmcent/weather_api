from django.urls import path
from .views import *


urlpatterns = [
    path('', WeatherUpdateView.as_view(),)
]