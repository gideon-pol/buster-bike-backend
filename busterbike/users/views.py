from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User

from .models import UserDetails
from bikes.models import Bike

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
                'capabilities': bike.capabilities["features"],
                'created_at': bike.created_at,
                'updated_at': bike.updated_at,
            }
            return JsonResponse(response, safe=False)
        
        return JsonResponse("", safe=False, status=200)