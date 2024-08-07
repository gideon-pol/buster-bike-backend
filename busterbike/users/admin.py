from django.contrib import admin

# Register your models here.
from .models import UserDetails, Referral

admin.site.register(UserDetails)
admin.site.register(Referral)