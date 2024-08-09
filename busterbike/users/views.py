from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.db import transaction

from .models import UserDetails, Referral
from bikes.models import Bike, Ride

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import random
from rest_framework.authtoken.models import Token
from geopy import distance

class BikeEndValidator(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    capabilities = serializers.DictField(required=True, child=serializers.IntegerField(required=True))
    latitude = serializers.DecimalField(required=True, max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(required=True, max_digits=9, decimal_places=6)
    notes = serializers.CharField(required=False, max_length=400)
    driven_distance = serializers.DecimalField(required=True, max_digits=9, decimal_places=2)

class ReservedBikeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bike = Bike.objects.filter(reserved_by=request.user).first()

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
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return JsonResponse({'success': 'User logged out'}, status=200)

class ReservedBikeEndView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BikeEndValidator(data=request.json)
        if not serializer.is_valid():
            return JsonResponse({'error': 'Invalid request'}, status=400)
        
        try:
            bike = Bike.objects.select_for_update().get(uuid=serializer.validated_data['id'])
            ride = Ride.objects.get(bike=bike, user=request.user, end_time=None)
        except Exception as e:
            return JsonResponse({'error': 'No bike reserved'}, status=404)

        bike.reserved_by = None
        bike.last_used_by = request.user
        bike.last_used_on = timezone.now()
        bike.capabilities = serializer.validated_data['capabilities']
        bike.latitude = serializer.validated_data['latitude']
        bike.longitude = serializer.validated_data['longitude']
        bike.notes = serializer.validated_data['notes']

        bike.save()

        start_point = (ride.start_latitude, ride.start_longitude)
        end_point = (serializer.validated_data['latitude'], serializer.validated_data['longitude'])

        dst = distance.distance(start_point, end_point).km

        if dst < 0.1 and serializer.validated_data['driven_distance'] < 0.1:
            ride.delete()
        else:
            ride.end_time = timezone.now()
            ride.end_latitude = bike.latitude
            ride.end_longitude = bike.longitude
            ride.distance = serializer.validated_data['driven_distance']
            ride.duration = ride.end_time - ride.start_time

            ride.save()

        return JsonResponse({'success': 'Bike reserved'}, status=200)
    
class RegisterValidator(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=10)
    password = serializers.CharField(required=True, max_length=128)
    referral_code = serializers.CharField(required=True, max_length=6, min_length=6)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        
        return value

    def validate_referral_code(self, value):
        if not value.isalnum():
            raise serializers.ValidationError('Invalid referral code')
        
        # referral_user = UserDetails.objects.filter(referral_code=value).first()
        # if not referral_user:
        #     raise serializers.ValidationError('Invalid referral code')

        referral = Referral.objects.filter(code=value).first()
        if not referral:
            raise serializers.ValidationError('Invalid referral code')
        
        if referral.referred:
            raise serializers.ValidationError('Referral code already used')
        
        return value
    
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterValidator(data=request.json)
        if not serializer.is_valid():
            print(serializer.errors)
            return JsonResponse({'error': serializer.errors}, status=400)
        
        with transaction.atomic():
            user = User.objects.create_user(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            user.first_name = serializer.validated_data['username']
            user.save()

            user_details = UserDetails(user=user)
            user_details.save()

            referral = Referral.objects.filter(code=serializer.validated_data['referral_code']).first()
            referral.referred = user
            referral.save()
            
            token, _ = Token.objects.get_or_create(user=user)
            response = {
                'success': 'User created',
                'token': token.key
            }

            return JsonResponse(response, status=200)
    
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user_details = UserDetails.objects.filter(user=request.user).first()

        referral = Referral.objects.filter(referred=request.user).first()

        response = {
            'id': request.user.id,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            # 'referral_code': user_details.referral_code,
            'referrer': referral.referrer.username if referral else None,
            'can_refer': request.user.has_perm("users.add_referral"),
            'created_at': request.user.date_joined,
            'updated_at': request.user.last_login,
            'permissions': [
                'bike.add' if request.user.has_perm("bike.add_bike") else None
            ]
        }

        return JsonResponse(response, safe=False)
    
class DeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.delete()
        return JsonResponse({'success': 'User deleted'}, status=200)
    
class ReferralCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.has_perm("users.add_referral"):
            return JsonResponse({'error': 'User does not have permission to create referral'}, status=403)
        
        referral_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        while Referral.objects.filter(code=referral_code).exists():
            referral_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        
        referral = Referral(code=referral_code, referrer=request.user)
        referral.save()

        return JsonResponse({'referral_code': referral_code}, status=201)
    
class ReferralListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        referrals = Referral.objects.filter(referrer=request.user)
        response = []
        for referral in referrals:
            response.append({
                'code': referral.code,
                'referred': referral.referred.username if referral.referred else None,
                'created_at': referral.created_at,
            })
        
        return JsonResponse(response, safe=False)