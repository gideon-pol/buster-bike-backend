from django.db import models
from django.contrib.auth.models import User

from bikes.models import Bike

import uuid

class UserDetails(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # referrer = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='referrer', blank=True, null=True)

    # referral_code = models.CharField(max_length=6, unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Referral(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)

    code = models.CharField(max_length=6, unique=True)

    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrer')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)