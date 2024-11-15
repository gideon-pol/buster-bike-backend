# Generated by Django 5.0.6 on 2024-06-15 19:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_userdetails_reserved_bike'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='referral_code',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='referrer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referrer', to=settings.AUTH_USER_MODEL),
        ),
    ]
