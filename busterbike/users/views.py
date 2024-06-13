from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User

from .models import UserDetails
from bikes.models import Bike

from rest_framework import serializers

class BikeEndValidator(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    capabilities = serializers.DictField(required=True, child=serializers.IntegerField(required=True))
    notes = serializers.CharField(required=False, max_length=400)

class ReservedBikeView(View):
    def get(self, request):
        user = User.objects.filter(is_superuser=True).first()
        user_details = UserDetails.objects.filter(user=user).first()

        bike = Bike.objects.filter(reserved_by=user).first()

        if(bike):
            response = {
                'id': bike.uuid,
                'name': bike.name,
                'code': bike.code,
                'latitude': bike.latitude,
                'longitude': bike.longitude,
                'is_available': bike.is_available,
                'is_in_use': True,
                'last_used_by': bike.last_used_by.first_name if bike.last_used_by else None,
                'last_used_on': bike.last_used_on,
                'capabilities': bike.capabilities,
                'notes': bike.notes,
                'created_at': bike.created_at,
                'updated_at': bike.updated_at,
            }
            return JsonResponse(response, safe=False)
        
        return JsonResponse("", safe=False, status=200)
    
class ReservedBikeEndView(View):
    def post(self, request):
        user = User.objects.filter(is_superuser=True).first()

        print(request.json)
        serializer = BikeEndValidator(data=request.json)
        if not serializer.is_valid():
            print(serializer.errors)
            return JsonResponse({'error': 'Invalid request'}, status=400)

        try:
            bike = Bike.objects.select_for_update().get(uuid=serializer.validated_data['id'])
        except Bike.DoesNotExist:
            return JsonResponse({'error': 'No bike reserved'}, status=404)
        
        bike.reserved_by = None
        bike.last_used_by = user
        bike.last_used_on = timezone.now()
        bike.capabilities = serializer.validated_data['capabilities']
        bike.notes = serializer.validated_data['notes']

        bike.save()

        return JsonResponse({'success': 'Bike reserved'}, status=200)