from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView 

from .models import Bike, Ride
from django.db import transaction, models

from random import choice

class ListBikesView(View):
    def get(self, request):
        bikes = Bike.objects.filter(is_available=True)
        bikes_list = []

        for bike in bikes:
            if bike.reserved_by:
                continue
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
                'total_distance': Ride.objects.filter(bike=bike).aggregate(models.Sum('distance'))['distance__sum'],
                'notes': bike.notes,
                'created_at': bike.created_at,
                'updated_at': bike.updated_at,
            })
        return JsonResponse(bikes_list, safe=False)
    
class ReserveBikeView(APIView):
    permission_classes = [IsAuthenticated]
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
            
            bike.reserved_by = request.user
            bike.last_used_by = request.user
            bike.last_used_on = timezone.now()
            bike.total_rides += 1

            bike.save()

            Ride.objects.create(
                bike=bike,
                user=request.user,
                start_time=timezone.now(),
                end_time=None,
                start_latitude=bike.latitude,
                start_longitude=bike.longitude,
                end_latitude=0,
                end_longitude=0,
                distance=0,
                duration=timedelta(seconds=0)
            )

        return JsonResponse({'success': 'Bike reserved'}, status=200)
    
class ImageBikeView(View):
    def get(self, request, bike_id):
        try:
            bike = Bike.objects.get(uuid=bike_id)
        except Bike.DoesNotExist:
            return JsonResponse({'error': 'Bike does not exist'}, status=404)
        
        image_data = open(f"bikes/images/{bike_id}.png", "rb").read()
        return HttpResponse(image_data, content_type="image/png", status=200)
    
class AddBikeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if not request.user.has_perm("bike.add_bike"):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        bike = Bike.objects.create(
            name=request.data['name'],
            code=''.join(choice('0123456789') for i in range(6)),
            latitude=request.data['latitude'],
            longitude=request.data['longitude'],
            is_available=True,
            reserved_by=None,
            last_used_by=None,
            last_used_on=None,
            capabilities=request.data['capabilities'],
            notes=request.data['notes']
        )
        bike.save()
        return JsonResponse({'success': 'Bike added'}, status=200)
