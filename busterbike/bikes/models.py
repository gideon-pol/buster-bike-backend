from django.db import models
from django.contrib.auth.models import User


from django.contrib.auth.models import User

import uuid

class Bike(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    is_available = models.BooleanField(default=True)
    # is_in_use = models.BooleanField(default=False)
    reserved_by = models.OneToOneField(User, null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name="reserved_by")

    capabilities = models.JSONField(default=dict)

    notes = models.CharField(max_length=400, default="Geen notities")

    last_used_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    last_used_on = models.DateTimeField(null=True, blank=True)

    total_rides = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Ride(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)

    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)

    distance = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    duration = models.DurationField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)