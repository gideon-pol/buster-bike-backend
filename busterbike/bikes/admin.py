from django.contrib import admin

# Register your models here.
from .models import Bike, Ride

admin.site.register(Bike)
admin.site.register(Ride)