from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from config.weather import process_weather
from django.utils.text import slugify

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin


# Create your views here.

class WeatherUpdateView(APIView):
    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        
        query = request.GET.get('query', None)
        
        if query is None:
            all_weather = WeatherUpdate.objects.all().order_by('-created_at')
            return Response(WeatherUpdateSerializer(all_weather, many=True).data, status=200)
        data, status = process_weather(query)
        
        if status == True:
            slug = slugify(data['location']['name'])
            try:
                weather = WeatherUpdate.objects.get(slug=slug)
                weather.location = data['location']
                weather.current = data['current']
                weather.save()
                
                return Response(WeatherUpdateSerializer(weather).data)
            
            except WeatherUpdate.DoesNotExist:
                weather = WeatherUpdate.objects.create(
                    country=data['location']['name'],
                    location=data['location'],
                    current=data['current']
                )
                return Response(WeatherUpdateSerializer(weather).data)
        else:
            return Response(data, status=404)