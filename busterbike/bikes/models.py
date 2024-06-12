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

    last_used_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    last_used_on = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
