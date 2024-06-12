from django.db import models
from django.contrib.auth.models import User

from bikes.models import Bike


import uuid

class UserDetails(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

