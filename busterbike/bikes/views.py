from django.utils import timezone
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from users.models import UserDetails

from .models import Bike
from django.db import transaction

from random import choice
import os

class ListBikesView(View):
    def get(self, request):
        bikes = Bike.objects.filter(is_available=True)
        bikes_list = []

        for bike in bikes:
            bikes_list.append({
                'id': bike.uuid,
                'name': bike.name,
                # 'code': bike.code,
                'latitude': bike.latitude,
                'longitude': bike.longitude,
                'is_available': bike.is_available,
                'is_in_use': bike.reserved_by != None,
                'last_used_by': bike.last_used_by.first_name if bike.last_used_by else None,
                'last_used_on': bike.last_used_on,
                'capabilities': bike.capabilities,
                'created_at': bike.created_at,
                'updated_at': bike.updated_at,
            })
        return JsonResponse(bikes_list, safe=False)
    
class ReserveBikeView(View):
    def post(self, request, bike_id):
        with transaction.atomic():
            try:
                bike = Bike.objects.select_for_update().get(uuid=bike_id)
            except Bike.DoesNotExist:
                return JsonResponse({'error': 'Bike does not exist'}, status=404)
            
            if not bike.is_available:
                return JsonResponse({'error': 'Bike is not available'}, status=400)
            if bike.reserved_by:
                return JsonResponse({'error': 'Bike is in use'}, status=400)
            
            user = User.objects.filter(is_superuser=True).first()

            bike.reserved_by = user
            bike.last_used_by = user
            bike.last_used_on = timezone.now()

            bike.save()

        return JsonResponse({'success': 'Bike reserved'}, status=200)
    
class ImageBikeView(View):
    def get(self, request, bike_id):
        try:
            bike = Bike.objects.get(uuid=bike_id)
        except Bike.DoesNotExist:
            return JsonResponse({'error': 'Bike does not exist'}, status=404)
        
        image_data = open(f"bikes/images/{bike_id}.png", "rb").read()
        return HttpResponse(image_data, content_type="image/png", status=200)